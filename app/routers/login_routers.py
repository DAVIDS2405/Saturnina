from fastapi import APIRouter, status
from app.controllers.user_controller import LoginData,Login
router = APIRouter(
    tags=["Usuario"],
)
#login to saturnina
@router.post("/login",status_code=status.HTTP_200_OK)
async def Iniciar_sesión_usuario(data: LoginData):
    response = await Login(data)
    return response

#user can register to saturnina
@router.post("/register")
async def Registro_usuario():
    return "Hello world"
#send the email if the user register and confirm the account
@router.get("/check-email/{token}")
async def Confirmar_cuenta():
    return "Hello world"

#check the token to the password and post the user to recover the password if user not remember the password
@router.post("/recover-password")
async def Confirmar_cuenta():
    return "Hello world"

@router.get("/recover-password/{token}")
async def Confirmar_cuenta():
    return "Hello world"

#update the password of the user 
@router.post("/new-password/{token}")
async def Confirmar_cuenta():
    return "Hello world"

#get the profile of the user to see the details
@router.get("/profile")
async def Confirmar_cuenta():
    return "Hello world"

#update the password of the user

@router.put("/update-password/{token}")
async def Confirmar_cuenta():
    return "Hello world"

#user get the user id  and update the profile

@router.get("/user/{id}")
async def Confirmar_cuenta():
    return "Hello world"

@router.put("/user/{id}")
async def Confirmar_cuenta():
    return "Hello world"


