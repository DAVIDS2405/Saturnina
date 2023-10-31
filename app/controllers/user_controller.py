import json
from fastapi import HTTPException,status
from config.smtp_config import smtp_config
from database.database import Connection
from helpers.jwt_helper import signJWT
from models.user_model import User_DB, User_Recover_Password
    
async def Login(data):
    
    email = data.email
    password = data.password
    
    user = None
    User_Db = await Connection()
    Check_user = await User_Db.select("user_saturnina")
    
    
    for user in Check_user:
        if(user.get("email")==email):
            user = user
            break
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"Usuario no registrado"})
     
    if user.get("email") != email:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"El correo es incorrecto"})
    
    if user.get("confirmEmail") is not True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Necesitas activar tu cuenta revisa tu correo para confirmar"})
    
    data_user_keys = {"nombre", "apellido", "telefono", "dirrecion", "id", "email", "token"}
    data_user_filtered = {key: user[key] for key in data_user_keys if key in user}
    data_user_filtered['token'] = signJWT(data_user_filtered['id']) 
    
    check_password = User_DB.verify_password(plain_password=password,password_bd=user.get("password"))
    
    if(check_password is not True):
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"La contraseña es incorrecta intenta de nuevo"})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=data_user_filtered)
    
    
async def Register(data): 
  
    email = data.email
    User_Db = await Connection()
    Check_email = await User_Db.select("user_saturnina")
    
    for user in Check_email:
         if(user["email"] == email):
             await User_Db.close()
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg":"Este email ya se encuentra en uso"})
    
    
    new_User = User_DB(**data.dict())
    new_User.password =  new_User.encrypt_password()
    
    token = new_User.generate_token()

    new_User = new_User.dict()
    new_User['password'] = new_User['password'].decode("utf-8")

    await User_Db.create("user_saturnina",new_User,)
        
    await User_Db.close()
        
    email_sender = smtp_config()
    email_sender.send_user(user_mail=email,token=token) 
        
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail={'msg':"Revisa tu correo para activar tu cuenta"})

async def Check_email(data):
    
    User_Db = await Connection()
    
    token_user = await User_Db.select("user_saturnina")
    user = None
    
    for user in token_user:
        if(user.get("token") == data):
            user = user
            break
     
    if user is None:
        await User_DB.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta cuenta no existe"})
        
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})

    elif user.get("token") != data:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})


    
    await User_Db.query('update ($id) merge {"token":null,"confirmEmail":true};' ,{"id":user.get("id")})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Ya puedes iniciar sesión"})
  

async def Recover_Password (data):
    email = data.email
    User_Db = await Connection()
    
    email_user_register = await User_Db.select("user_saturnina")
    
    user = None
    
    for user in email_user_register:
        if(user.get("email") == email):
            user = user
            break
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"Usuario no registrado"})
    
    if user.get('confirmEmail') is not True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"Necesita activar su cuenta"})
    
    new_User = User_DB(**user)
    token = new_User.generate_token()

    await User_Db.query('update ($id) merge {"token":($token_new),"confirmEmail":false};' ,{"id":user.get("id"),"token_new":token})
    await User_Db.close()

    email_sender = smtp_config()
    email_sender.Recover_password(user_mail=email,token=token)
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail={'msg':"Revisa tu correo para recuperar tu contraseña"})

async def Check_token(data):
    
    User_Db = await Connection()
    
    token_user = await User_Db.select("user_saturnina")
    user = None
    
    for user in token_user:
        if(user.get("token") == data):
            user = user
            break
    
    if user is None:
        await User_DB.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta cuenta no existe"})
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})

    elif user.get("token") != data:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})
    
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Token confirmado ya puedes crear tu nueva contraseña"})

async def New_password(token,data):
    new_password = data.new_password
    check_new_password = data.check_password
    User_Db = await Connection()
    user = None
    
    check_token = await User_Db.select("user_saturnina")
    if(new_password != check_new_password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Las password no coinciden"})
    
    for user in check_token:
        if(user.get('token') == token):
            user = user
            break
    
    if user is None:
        await User_DB.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"Esta cuenta no existe"})
    
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})
    
    if user.get("token") != token:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})
    

    new_User = User_Recover_Password(**data.dict())
    
    new_User.new_password = new_User.encrypt_password()
    new_User = new_User.dict()
    new_User['new_password'] = new_User['new_password'].decode("utf-8")
    password = new_User['new_password']
    
    await User_Db.query('update ($id) merge {"token":null,"confirmEmail":true,"password":($password_new)};' ,{"id":user.get("id"),"password_new":password})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Tu contraseña a sido actualizada ya puedes iniciar sesión"})


async def User_profile(data):
    data = data[1]
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=data)

async def User_profile_actualizar_contrasenia(password,data):
    data = data[1]
    new_password = password.new_password
    check_new_password = password.check_password
    id_user = data.get('id')
    User_Db = await Connection()
    user_update_password = await User_Db.select(id_user)
    
    if(new_password != check_new_password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"Las password no coinciden"})
    
    if user_update_password is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg":"No existe este usuario"})
    
    new_User = User_Recover_Password(**password.dict())

    new_User.new_password = new_User.encrypt_password()
    new_User = new_User.dict()
    new_User['new_password'] = new_User['new_password'].decode("utf-8")
    password = new_User['new_password']
    
    check_password = User_DB.verify_password(plain_password=check_new_password,password_bd=user_update_password['password'])
    
    if check_password is  True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"La contraseña es igual a la anterior"})
    

    
    await User_Db.query('update ($id) merge {"password":($password_new)};' ,{"id":id_user,"password_new":password})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Tu contraseña a sido actualizada"})

async def User_detail(id):
    User_Db = await Connection()
    
    user = await User_Db.select(id)
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"no se encuentra el Usuario"})
    
    data_user_keys = {"nombre", "apellido", "telefono", "dirrecion", "id", "email"}
    data_user_filtered = {key: user[key] for key in data_user_keys if key in user}
    
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=data_user_filtered)

async def User_detail_Update(id,data):
    User_Db = await Connection()
    user = await User_Db.select(id)
        
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"no se encuentra el Usuario"})
    

    new_email_user = data.email
    new_telefono = data.telefono
    new_apellido = data.apellido
    new_direccion =data.direccion
    new_nombre = data.nombre
    
    await User_Db.query('update ($id) merge {"nombre":($new_name),"apellido":($new_lastname),"direccion":($new_address),"telefono":($new_phone),"email":($new_email)};' ,{"id":user.get("id"),"new_name":new_nombre,"new_lastname":new_apellido,"new_address":new_direccion,"new_phone":new_telefono,"new_email":new_email_user})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"msg":"Datos actualizados correctamente"})