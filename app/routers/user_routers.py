from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, Request, UploadFile, File
from middlewares.check_admin_user_JWT import Check_rol_user
from controllers.user_controller import Check_email, Check_token, Create_comments, Create_order, Get_comments, Get_comments_user, Login, New_password, Recover_Password, Register, Update_comments, Update_order, User_detail, User_detail_Update, User_profile, User_profile_actualizar_contrasenia, View_order
from models.user_model import Comment_product, Email_User, Order, Order_update, User_Login, User_Recover_Password, User_Register, User_Update
from middlewares.Bearer import JWTBearer

router = APIRouter(
    tags=["Usuario"]
)


@router.post("/login", description="Inicia sesión con tu correo y contraseña")
async def Iniciar_sesión_usuario(data: User_Login = Body(examples=[
    {"email": "sebastian2405lucero@hotmail.com",
     "password": "@asdaw@qweDb"
    }]

)):
    response = await Login(data)
    return response


@router.post("/register", description="Crea un usuario con los siguientes datos")
async def Registro_usuario(data: User_Register = Body(examples=[{
    "nombre": "David",
    "apellido": "Basantes",
    "email": "sebastian2405lucero@hotmail.com",
    "telefono": "090095964",
    "password": "@asdaw@qweDb"

}])):
    response = await Register(data)
    return response


@router.get("/check-email/{token}")
async def Confirmar_cuenta(token: str):
    response = await Check_email(token)
    return response


@router.post("/recover-password")
async def Recuperar_Contrasenia(data: Email_User = Body(examples=[{
    "email": "sebastian2405lucero@hotmail.com"
}])):
    response = await Recover_Password(data)
    return response


@router.get("/recover-password/{token}")
async def Confirmar_cuenta(token: str):
    response = await Check_token(token)
    return response


@router.post("/new-password/{token}")
async def Nueva_Contrasenia(token: str, password: User_Recover_Password = Body(examples=[{
    "new_password": "change123",
    "check_password": "change123"
}])):
    response = await New_password(token, password)
    return response


@router.get("/profile", dependencies=[Depends(JWTBearer())])
async def User_Perfil(token: Request):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await User_profile(token[1])
    return response


@router.put("/update-password", dependencies=[Depends(JWTBearer())])
async def Actualizar_contrasenia(token: Request, password: User_Recover_Password = Body(examples=[{
    "new_password": "change123",
    "check_password": "change123"
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await User_profile_actualizar_contrasenia(password,token[1])
    return response


@router.get("/user/{id}", dependencies=[Depends(JWTBearer())])
async def Datos_cuenta(id: str, token: Request):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await User_detail(id)
    return response


@router.put("/user/{id}", dependencies=[Depends(JWTBearer())])
async def Actualizar_Perfil(id: str, token: Request, data: User_Update = Body(examples=[{
    "nombre": "Sebastian",
    "apellido": "Lucero",
    "telefono": "0990095963",
    "email": "sebastian2405lucero@gmail.com"
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await User_detail_Update(id, data)
    return response


@router.get("/order/{id_user}", dependencies=[Depends(JWTBearer())])
async def Buscar_pedido(id_user: str, token: Request):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await View_order(id_user)
    return response


@router.post("/order", dependencies=[Depends(JWTBearer())])
async def Crear_pedido(token: Request, data: Order = Body(), transfer_image: UploadFile = File()):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await Create_order(data, transfer_image)
    return response


@router.put("/order/{id_order}", dependencies=[Depends(JWTBearer())])
async def Actualizar_orden(id_order: str, token: Request,transfer_image: UploadFile | None = None, data: Order_update = Body() ):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await Update_order(id_order, data, transfer_image)
    return response


@router.get("/comments")
async def Todos_comentarios():
    response = await Get_comments()
    return response


@router.get("/comments/{user_id}", dependencies=[Depends(JWTBearer())])
async def Todos_comentarios_usuario(user_id: str, token: Request):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await Get_comments_user(user_id)
    return response


@router.post("/comments", dependencies=[Depends(JWTBearer())])
async def Crear_comentario_producto(token: Request, data: Comment_product = Body(examples=[{
    "descripcion": "Me gusto mucho la decoracion les recomiendo",
    "user_id": "user_saturnina:duarv161uh97q49gus2r",
    "id_producto": "product:56btylsbf10jruqzh0da",
    "calificacion": 2
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await Create_comments(data)
    return response


@router.put("/comments/{id_comment}", dependencies=[Depends(JWTBearer())])
async def Actualizar_comentario_producto(id_comment: str, token: Request, data: Comment_product = Body(examples=[{
    "descripcion": "Me gusto mucho la decoracion les recomiendo",
    "user_id": "user_saturnina:duarv161uh97q49gus2r",
    "id_producto": "product:56btylsbf10jruqzh0da",
    "calificacion": 2
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_user(token[1])
    response = await Update_comments(data, id_comment)
    return response

