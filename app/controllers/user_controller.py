from fastapi import HTTPException,status
from app.config.smtp_config import smtp_config
from app.database.database import Connection
from app.helpers.jwt_helper import signJWT
from app.models.user_model import User_DB
    
async def Login(data):
    
    email = data.email
    password = data.password
    
    user = None
    User_Db = await Connection()
    Check_user = await User_Db.select("user_saturnina")
    
    for user in Check_user:
        if(user["email"]==email):
            user = user
            break

            
    
    if user is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail={"msg":"Usuario no registrado"}) 
    
    if user.get("confirmEmail") is not True:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "Necesitas activar tu cuenta revisa tu correo para confirmar"})
    
    data_user_keys = {"nombre", "apellido", "password_requiered", "telefono", "dirrecion", "id", "email", "token"}
    data_user_filtered = {key: user[key] for key in data_user_keys if key in user}
    data_user_filtered['token'] = signJWT(data_user_filtered['id']) 
    data_user_filtered = str(data_user_filtered)
    check_password = User_DB.verify_password(plain_password=password,password_bd=user.get("password"))
    
    
    if(check_password is not True):
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail={"msg":"La contraseñas es incorrecta intenta de nuevo"})
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

async def Confirm_email(data):
    
    User_Db = await Connection()
    
    token_user = await User_Db.select("user_saturnina")
    user = None
    
    for user in token_user:
        if(user.get("token") == data):
            user = user
            break
        
    if user.get("token") is None:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={"msg":"La cuenta ya ha sido confirmada"})

    elif user.get("token") != data:
        await User_Db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Lo sentimos, no se puede validar la cuenta"})


    
    await User_Db.query('update ($id) merge {"token":null,"confirmEmail":true};' ,{"id":user.get("id")})
    await User_Db.close()
    raise HTTPException(status_code=status.HTTP_200_OK, detail={"msg":"Ya puedes iniciar sesion"})
  
async def detail_User (data):
    id = data.id
    