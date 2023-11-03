from fastapi import APIRouter,Body, Depends
from controllers.admin_controller import Create_category, Delete_category, List_category, Update_category
from models.category_products import Category
from middlewares.Bearer import JWTBearer

router = APIRouter(
    tags=["Administrador"],
)

@router.get("/category")
async def Listar_categorias():
    response = await List_category()
    return response

@router.post("/category", )
async def Crear_categorias(data: Category = Body(example={
    "name": "Reparación de ropa"
})):
    response = await Create_category(data)
    return response

@router.put("/category/{id_category}")
async def Actualizar_categoria(id_category:str, data:Category = Body(example={
    "name":"Reparacion de ropa"
})):
    response = await Update_category(id_category,data)
    return response
@router.delete("/category/{id_category}")
async def Elimar_categorua(id_category:str):
    response = await Delete_category(id_category)
    return response
