# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
import os
import jwt
from database.database import Connection

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")


async def Search_User(id):
    User_Db = await Connection()
    user = await User_Db.select(id)
    data_user_keys = {"nombre", "apellido", "telefono", "direccion", "id", "email","is_admin"}
    data_user_filtered = {key: user[key] for key in data_user_keys if key in user}
    await User_Db.close()
    return data_user_filtered

# function used for signing the JWT string
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 1000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


async def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        id = decoded_token['user_id']
        user = await Search_User(id)
        return (decoded_token,user) if decoded_token["expires"] >= time.time() else None
    except:
        return {}