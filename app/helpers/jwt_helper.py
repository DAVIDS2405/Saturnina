# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict
import os
import jwt
from database.database import Connection

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")




# function used for signing the JWT string
def signJWT(user_id: str,user_rol:str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "rol":user_rol,
        "expires": time.time() + 1800
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


async def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


        return (decoded_token) if decoded_token["expires"] >= time.time() else None
    except:
        return {}