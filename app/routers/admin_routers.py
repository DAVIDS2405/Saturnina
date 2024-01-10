from typing import Optional
from fastapi import APIRouter,Body, Depends, File, Request, UploadFile
from middlewares.check_admin_user_JWT import Check_rol_admin
from controllers.admin_controller import Create_category, Create_products, Delete_comments, Delete_products, Delete_category, Get_all_orders, Get_one_products, Get_products, List_category, Update_category, Update_order_status, Update_products
from models.admin_model import Category,  Order_update_status, Products
from middlewares.Bearer import JWTBearer


router = APIRouter(
    tags=["Administrador"],
)



@router.get("/category")
async def Listar_categorias():
    response = await List_category()
    return response

@router.post("/category", dependencies=[Depends(JWTBearer())])
async def Crear_categoria(token: Request,data: Category = Body(examples=[{
    "name": "Reparación de ropa"
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Create_category(data)
    return response

@router.put("/category/{id_category}",dependencies=[Depends(JWTBearer())])
async def Actualizar_categoria(token: Request,id_category:str, data:Category = Body(examples=[{
    "name":"Reparacion de ropa"
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Update_category(id_category,data)
    return response

@router.delete("/category/{id_category}",dependencies=[Depends(JWTBearer())])
async def Elimar_categoria(id_category: str, token: Request):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Delete_category(id_category)
    return response

@router.get("/products")
async def Obtener_Productos():
    response = await Get_products()
    return response


@router.get("/products/{id_products}")
async def Obtener_Productos(id_products : str):
    response = await Get_one_products(id_products)
    return response


@router.post("/products", dependencies=[Depends(JWTBearer())])
async def Crear_Producto(token: Request, imagen_producto: list[UploadFile], data: Products = Body(),):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Create_products(data,imagen_producto)
    return response

@router.put("/products/{id_product}",dependencies=[Depends(JWTBearer())])
async def Actualizar_producto(id_product: str, token: Request, imagen_producto: list[UploadFile] = File(None),data: Products = Body(...)):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response  = await Update_products(id_product,data,imagen_producto)
    return response
    
@router.delete("/products/{id_product}",dependencies=[Depends(JWTBearer())])
async def Eliminar_Producto(id_product: str, token: Request):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Delete_products(id_product)
    return response

@router.get("/orders",dependencies=[Depends(JWTBearer())])
async def Obtener_ordenes(token:Request):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Get_all_orders()
    return response

@router.put("/orders/{id_order_detail}",dependencies=[Depends(JWTBearer())])
async def Actualizar_orden_status(id_order_detail: str, token: Request, data: Order_update_status = Body(examples=[{
    "status_order": "Rechazado",
    "descripcion": "Se ha rechazado tu orden ",
}])):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Update_order_status(id_order_detail, data)
    return response



@router.delete("/comments/{id_comment}",dependencies=[Depends(JWTBearer())])
async def Eliminar_comentario(token: Request,id_comment:str):
    token = token.headers.get("authorization").split()
    await Check_rol_admin(token[1])
    response = await Delete_comments(id_comment)
    return response