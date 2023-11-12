from fastapi import APIRouter,Body, Depends, File, UploadFile
from controllers.admin_controller import Create_category, Create_products, Delete_products, Delete_category, Get_products, List_category, Update_category, Update_products
from models.admin_model import Category, Products
from middlewares.Bearer import JWTBearer


router = APIRouter(
    tags=["Administrador"],
)



@router.get("/category")
async def Listar_categorias():
    response = await List_category()
    return response

@router.post("/category", dependencies=[Depends(JWTBearer())])
async def Crear_categoria(data: Category = Body(example={
    "name": "Reparación de ropa"
})):
    response = await Create_category(data)
    return response

@router.put("/category/{id_category}",dependencies=[Depends(JWTBearer())])
async def Actualizar_categoria(id_category:str, data:Category = Body(example={
    "name":"Reparacion de ropa"
})):
    response = await Update_category(id_category,data)
    return response
@router.delete("/category/{id_category}",dependencies=[Depends(JWTBearer())])
async def Elimar_categoria(id_category:str):
    response = await Delete_category(id_category)
    return response

@router.get("/products")
async def Obtener_Productos():
    response = await Get_products()
    return response


@router.post("/products", dependencies=[Depends(JWTBearer())])
async def Crear_Producto( data:Products = Body(),
    imagen_producto: UploadFile = File()):
    response = await Create_products(data,imagen_producto)
    return response

@router.put("/products/{id_product}",dependencies=[Depends(JWTBearer())])
async def Actualizar_producto(id_product:str,data:Products = Body(...),imagen_producto: UploadFile = File(...)):
    response  = await Update_products(id_product,data,imagen_producto)
    return response
    
@router.delete("/products/{id_product}",dependencies=[Depends(JWTBearer())])
async def Eliminar_Producto(id_product:str):
    response = await Delete_products(id_product)
    return response