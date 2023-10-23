from fastapi import HTTPException
from app.database.database import Connection
from app.models.user_model import LoginData


    
async def Login(data: LoginData):
    email = data.username.strip()
    password = data.password.strip()
    connection = await Connection()
    if not email or not password:
        
        raise HTTPException(status_code=400, detail={"msg":"Debes llenar todos los campos"})
    
    