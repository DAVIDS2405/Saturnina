from fastapi import APIRouter
router = APIRouter(
    prefix="/login",
    tags=["Registro"],
    responses={404: {"message": "No encontrado"}},
)


@router.get("/")
async def login():
    return "Hello world"


