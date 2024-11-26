from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from models import user_model
from services.user_services import UserService
from fastapi import HTTPException, Request, status
from config.cloudinary_config import Delete_image, Upload_image
from helpers.password.users_password import verify_password
from helpers.auth.JWT import create_token
from prisma import Prisma


templates = Jinja2Templates(directory="app/templates/")


async def login(data, request: Request):
    db_connection = Prisma()
    client = UserService(db_connection)
    user = dict(await client.exists(data.email))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'msg': "This user not exist"})

    verify_password(data.password, user.get('password'))

    if not user.get("confirm_email"):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='You need to confirm your email')

    user.pop('password')

    JWT = create_token(data=user)

    request.session['token'] = JWT

    user.pop('rol')
    user.pop('token')
    user.pop('confirm_email')

    raise HTTPException(status_code=status.HTTP_200_OK, detail=user)


async def register(data):
    db_connection = Prisma()
    client = UserService(db_connection)
    exist = await client.exists(data.email)

    if not exist:
        new_user = await client.create(data)
        raise new_user

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                        'msg': "This user exist"})


async def checkEmail(token: str, email: user_model):

    db_connection = Prisma()
    client = UserService(db_connection)
    user = dict(await client.exists(email.email))

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            'msg': "This user not exist"})

    if user.get('token') == '':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "msg": "La cuenta ya ha sido confirmada"})

    if token != user.get('token'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'We cannot validate your account '})

    user.update(confirm_mail=True, token='')

    await client.update(user)

    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "Ya puedes iniciar sesión"})


async def recoverPassword(data):
    email = data.email
    User_Db = await Connection()
    email_user_register = await User_Db.query('select * from user_saturnina where email =($user_email)', {"user_email": email})

    if not email_user_register[0].get('result'):
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "Usuario no registrado"})

    user = email_user_register[0].get('result')[0]

    if user.get('confirmEmail') is not True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "Necesita activar su cuenta"})

    new_User = Recover_Pass(**user)
    token = new_User.generate_token()

    await User_Db.query('update ($id) merge {"token":($token_new),"confirmEmail":false};', {"id": user.get("id"), "token_new": token})
    await User_Db.close()

    email_sender = smtp_config()
    email_sender.Recover_password(user_mail=email, token=token)
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail={
                        'msg': "Revisa tu correo para recuperar tu contraseña"})


async def Check_token(data):

    User_Db = await Connection()

    token_user = await User_Db.select("user_saturnina")
    user = None

    for user in token_user:
        if (user.get("token") == data):
            user = user
            break

    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Esta cuenta no existe"})
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "La cuenta ya ha sido confirmada"})

    elif user.get("token") != data:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Lo sentimos, no se puede validar la cuenta"})

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "Token confirmado ya puedes crear tu nueva contraseña"})


async def New_password(token, data):
    new_password = data.new_password
    check_new_password = data.check_password
    User_Db = await Connection()
    user = None

    check_token = await User_Db.select("user_saturnina")

    if new_password.get_secret_value() != check_new_password.get_secret_value():
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                            "msg": "Las password no coinciden"})

    for user in check_token:
        if (user.get('token') == token):
            user = user
            break

    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Esta cuenta no existe"})

    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "La cuenta ya ha sido confirmada"})

    if user.get("token") != token:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            "msg": "Lo sentimos, no se puede validar la cuenta"})

    new_User = User_Recover_Password(**data.dict())

    new_User.new_password = new_User.encrypt_password()
    new_User = new_User.dict()
    new_User['new_password'] = new_User['new_password'].decode("utf-8")
    password = new_User['new_password']

    await User_Db.query('update ($id) merge {"token":null,"confirmEmail":true,"password":($password_new)};', {"id": user.get("id"), "password_new": password})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "Tu contraseña a sido actualizada ya puedes iniciar sesión"})


async def User_profile(data: dict):
    UserDb = await Connection()
    decode_token = data

    if (decode_token.get('iss')):
        return decode_token

    check_user_db = await UserDb.select(decode_token.get("user_id"))

    if not check_user_db:
        await UserDb.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "msg": "El usuario no existe"})

    data_user_keys = {"nombre", "apellido", "telefono", "email"}
    data_user_filtered = {key: check_user_db[key]
                          for key in data_user_keys if key in check_user_db}
    await UserDb.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                        detail=data_user_filtered)


async def User_profile_actualizar_contrasenia(password, data):
    decode_token = await validate_token(data)
    new_password = password.new_password
    check_new_password = password.check_password
    id_user = decode_token.get('user_id')
    User_Db = await Connection()
    user_update_password = await User_Db.select(id_user)

    if not user_update_password:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "no se encuentra el Usuario"})

    if (new_password.get_secret_value() != check_new_password.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                            "msg": "Las password no coinciden"})

    if user_update_password is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "No existe este usuario"})

    new_User = User_Recover_Password(**password.dict())

    new_User.new_password = new_User.encrypt_password()
    new_User = new_User.dict()
    new_User['new_password'] = new_User['new_password'].decode("utf-8")
    password = new_User['new_password']

    check_password = User_DB.verify_password(
        plain_password=check_new_password, password_bd=user_update_password['password'])

    if check_password is True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail={
                            "msg": "La contraseña es igual a la anterior"})

    await User_Db.query('update ($id) merge {"password":($password_new)};', {"id": id_user, "password_new": password})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={
                        "msg": "Tu contraseña a sido actualizada"})


async def User_detail(id):
    User_Db = await Connection()

    user = await User_Db.select(id)

    if not user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "no se encuentra el Usuario"})

    data_user_keys = {"nombre", "apellido",
                      "telefono", "dirrecion", "id", "email"}
    data_user_filtered = {key: user[key]
                          for key in data_user_keys if key in user}

    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                        detail=data_user_filtered)


async def User_detail_Update(id, data):
    User_Db = await Connection()
    user = await User_Db.select(id)

    if not user:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
                            "msg": "no se encuentra el Usuario"})

    new_email_user = data.email
    new_telefono = data.telefono
    new_apellido = data.apellido
    new_nombre = data.nombre

    await User_Db.query('update ($id) merge {"nombre":($new_name),"apellido":($new_lastname),"telefono":($new_phone),"email":($new_email)};', {"id": user.get("id"), "new_name": new_nombre, "new_lastname": new_apellido, "new_phone": new_telefono, "new_email": new_email_user})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={
                        "msg": "Datos actualizados correctamente"})
