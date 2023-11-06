from fastapi import APIRouter,Body, Depends
from controllers.user_controller import Check_email, Check_token, Login, New_password, Recover_Password, Register, User_detail, User_detail_Update, User_profile, User_profile_actualizar_contrasenia
from models.user_model import Email_User, User_Login, User_Recover_Password, User_Register, User_Update
from middlewares.Bearer import JWTBearer

router = APIRouter(
    tags=["Usuario"]
)


@router.post("/login", description="Inicia sesión con tu correo y contraseña")
async def Iniciar_sesión_usuario(data:User_Login = Body(example={
    "email":"sebastian2405lucero@hotmail.com",
    "password":"@asdaw@qweDb"
})):
    response = await Login(data)
    return response

@router.post("/register",description="Crea un usuario con los siguientes datos")
async def Registro_usuario(data:User_Register = Body(example={
    "nombre":"David",
    "apellido":"Basantes",
    "email":"sebastian2405lucero@hotmail.com",
    "telefono":"090095964",
    "password":"@asdaw@qweDb"
    
})):
        response = await Register(data)  
        return response  


@router.get("/check-email/{token}")
async def Confirmar_cuenta(token: str):
    response = await Check_email(token)
    return response

@router.post("/recover-password")
async def Recuperar_Contrasenia(data:Email_User = Body(example={
    "email":"sebastian2405lucero@hotmail.com"
})):
    response = await Recover_Password(data)
    return response

@router.get("/recover-password/{token}")
async def Confirmar_cuenta(token:str):
    response = await Check_token(token)
    return response

@router.post("/new-password/{token}")
async def Nueva_Contrasenia(token:str,password:User_Recover_Password = Body(example={
    "new_password":"change123",
    "check_password":"change123"
})):
    response = await New_password(token,password)
    return response

@router.get("/profile")
async def User_Perfil(data: dict = Depends(JWTBearer())):
    response = await User_profile(data[1])
    return response


@router.put("/update-password")
async def Actualizar_contrasenia(password:User_Recover_Password = Body(example={
    "new_password":"change123",
    "check_password":"change123"
    }),data: dict = Depends(JWTBearer())):
    response = await User_profile_actualizar_contrasenia(password,data[1])
    return "usuario"


@router.get("/user/{id}",dependencies=[Depends(JWTBearer())])
async def Datos_cuenta(id:str):
    response = await User_detail(id)
    return response

@router.put("/user/{id}",dependencies=[Depends(JWTBearer())])
async def Actualizar_Perfil(id:str,data:User_Update = Body(example={
    "nombre":"Sebastian",
    "apellido":"Lucero",
    "telefono":"0990095963",
    "email":"sebastian2405lucero@gmail.com",
    "direccion":"Magdalena"
})):
    response = await User_detail_Update(id,data)
    return response

