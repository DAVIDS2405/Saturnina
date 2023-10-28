from fastapi import APIRouter,status,Body, Depends
from controllers.user_controller import Confirm_email, Login, Register
from models.user_model import User_Login, User_Register
from middlewares.Bearer import JWTBearer


router = APIRouter(
    tags=["Usuario"],
)


@router.post("/login",status_code=status.HTTP_200_OK)
async def Iniciar_sesión_usuario(data:User_Login = Body(example={
    "email":"sebastian2405lucero@hotmail.com",
    "password":"@asdaw@qweDb"
})):
    response = await Login(data)
    return response

@router.post("/register",status_code=status.HTTP_201_CREATED)
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
    response = await Confirm_email(token)
    return response

@router.post("/recover-password")
async def Confirmar_cuenta():
    return "Hello world"

@router.get("/recover-password/{token}")
async def Confirmar_cuenta():
    return "Hello world"

@router.post("/new-password/{token}")
async def Confirmar_cuenta():
    return "Hello world"

@router.get("/profile",dependencies=[Depends(JWTBearer())])
async def Confirmar_cuenta():
    return "Hello world"


@router.put("/update-password/{token}",dependencies=[Depends(JWTBearer())])
async def Confirmar_cuenta():
    return "Hello world"


@router.get("/user/{id}",dependencies=[Depends(JWTBearer())])
async def Confirmar_cuenta():
    
    return "Hello world"

@router.put("/user/{id}",dependencies=[Depends(JWTBearer())])
async def Confirmar_cuenta():
    return "Hello world"

