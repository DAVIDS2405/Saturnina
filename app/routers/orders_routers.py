from fastapi import APIRouter, Depends, Request
from controllers import user_controller
from helpers.auth.JWT import verify_rol
from middlewares.BearerCookie import JWTBearerCookie


router = APIRouter(
    tags=["Usuario"]
)


@router.get("/order/{id_user}", dependencies=[Depends(JWTBearerCookie)])
async def Buscar_pedido(id_user: str, token: Request):

    await verify_rol(token.session.get('token'))
    response = await user_controller.View_order(id_user)
    return response


@router.post("/order", dependencies=[Depends(JWTBearerCookie)])
async def Crear_pedido(token: Request, data: user_model.Order = Body(), transfer_image: UploadFile = File()):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Create_order(data, transfer_image)
    return response


@router.put("/order/{id_order}", dependencies=[Depends(JWTBearerCookie)])
async def Actualizar_orden(id_order: str, token: Request, transfer_image: UploadFile | None = None, data: user_model.Order_update = Body()):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await user_controller.Update_order(id_order, data, transfer_image)
    return response
