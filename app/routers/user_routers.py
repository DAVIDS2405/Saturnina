from fastapi import APIRouter, Body, Depends, Request, UploadFile, File
from middlewares.BearerCookie import JWTBearerCookie
from helpers.auth.JWT import verify_rol
from controllers import user_controller
from models import user_model
from middlewares.BearerCookie import JWTBearerCookie
router = APIRouter(
    tags=["Usuario"]
)


@router.post("/login", description="Inicia sesión con tu correo y contraseña")
async def userSession(response: Request, data: user_model.User_Login = Body(examples=[
    {"email": "sebastian2405lucero@hotmail.com",
     "password": "@asdaw@qweDb"
     }]

)):
    response = await user_controller.login(data, response)
    return response


@router.post("/register", description="Crea un usuario con los siguientes datos")
async def registerUser(data: user_model.User = Body(examples=[{
    "nombre": "David",
    "apellido": "Basantes",
    "email": "sebastian2405lucero@hotmail.com",
    "telefono": "090095964",
    "password": "@asdaw@qweDb"

}])):
    response = await user_controller.register(data)
    return response


@router.post("/check-email/{token}")
async def checkEmail(token: str, email: user_model.Email_User = Body(examples=[{
    "email": "sebastian2405lucero@hotmail.com"
}])):
    response = await user_controller.checkEmail(token, email)
    return response


@router.post("/recover-password")
async def recoverPassword(data: user_model.Email_User = Body(examples=[{
    "email": "sebastian2405lucero@hotmail.com"
}])):
    response = await user_controller.recoverPassword(data)
    return response


@router.get("/recover-password/{token}")
async def Confirmar_cuenta(token: str):
    response = await user_controller.Check_token(token)
    return response


@router.post("/new-password/{token}")
async def Nueva_Contrasenia(token: str, password: user_model.User_Recover_Password = Body(examples=[{
    "new_password": "change123",
    "check_password": "change123"
}])):
    response = await user_controller.New_password(token, password)
    return response


@router.get("/profile", dependencies=[Depends(JWTBearerCookie)])
async def User_Perfil(payload: dict = Depends(JWTBearerCookie)):
    response = await user_controller.User_profile(payload)
    return response


@router.put("/update-password", dependencies=[Depends(JWTBearerCookie)])
async def Update_Password(token: Request, password: user_model.User_Recover_Password = Body(examples=[{
    "new_password": "change123",
    "check_password": "change123"
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.User_profile_update_password(password, token[1])
    return response


@router.get("/user/{id}", dependencies=[Depends(JWTBearerCookie)])
async def Datos_cuenta(id: str, token: Request):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.User_detail(id)
    return response


@router.put("/user/{id}", dependencies=[Depends(JWTBearerCookie)])
async def Actualizar_Perfil(id: str, token: Request, data: user_model.User_Update = Body(examples=[{
    "nombre": "Sebastian",
    "apellido": "Lucero",
    "telefono": "0990095963",
    "email": "sebastian2405lucero@gmail.com"
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.User_detail_Update(id, data)
    return response


@router.delete("/user/{id}", dependencies=[Depends(JWTBearerCookie)])
async def Eliminar_Cuenta(id: str, token: Request):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    return "Correo Eliminado"
