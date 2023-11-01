from fastapi import APIRouter,status,Body, Depends


router = APIRouter(
    tags=["Administrador"],
)

@router.get("/category")
async def Obtener_Categorias():
    return "hello"
