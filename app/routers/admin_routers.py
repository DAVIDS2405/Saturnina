from typing import Optional
from fastapi import APIRouter, Body, Depends, File, Request, UploadFile
from helpers.auth.JWT import verify_rol
from controllers import admin_controller
from models.admin_model import Category,  Order_update_status, Products
from middlewares.BearerCookie import JWTBearerCookie


router = APIRouter(
    tags=["Administrador"],
)


@router.get("/orders", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def Obtener_ordenes(token: Request):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Get_all_orders()
    return response


@router.put("/orders/{id_order_detail}", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def Actualizar_orden_status(id_order_detail: str, token: Request, data: Order_update_status = Body(examples=[{
    "status_order": "Rechazado",
    "descripcion": "Se ha rechazado tu orden",
}])):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Update_order_status(id_order_detail, data)
    return response


@router.delete("/comments/{id_comment}", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def Eliminar_comentario(token: Request, id_comment: str):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Delete_comments(id_comment)
    return response


@router.delete("/comments-general/{id_comment}", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def Eliminar_comentario_general(token: Request, id_comment: str):
    token = token.headers.get("authorization").split()
    await verify_rol(token[1])
    response = await admin_controller.Delete_general_comments(id_comment)
    return response
