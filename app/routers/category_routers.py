from fastapi import APIRouter, Body, Depends, Request
from app.models.admin_model import Category
from helpers.auth.JWT import verify_rol
from middlewares.BearerCookie import JWTBearerCookie
from controllers import category_controller
router = APIRouter(
    tags=['Category']
)


@router.get("/category")
async def listCategorys():
    response = await category_controller.get_all()
    return response


@router.post("/category", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def createCategory(request: Request, data: Category = Body(examples=[{
    "name": "Reparación de ropa"
}])):
    response = await category_controller.create(data)
    return response


@router.put("/category/{id_category}", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def updateCategory(token: Request, id_category: str, data: Category = Body(examples=[{
    "name": "Reparacion de ropa"
}])):
    response = await category_controller.update(id_category, data)
    return response


@router.delete("/category/{id_category}", dependencies=[Depends(JWTBearerCookie, "Admin")])
async def deleteCategory(id_category: str):

    response = await category_controller.delete(id_category)
    return response
