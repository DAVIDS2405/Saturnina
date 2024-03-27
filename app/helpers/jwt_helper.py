from dotenv import load_dotenv
from http.client import HTTPException
import os
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, UTC

load_dotenv()

JWT_SECRET = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")


def signJWT(user_id: str, user_rol: str):
    payload = {
        "user_id": user_id,
        "rol": user_rol,
        "exp": datetime.now(UTC) + timedelta(minutes=30)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


async def decodeJWT(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        return payload

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="El Token ha expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except JWTError:

        raise HTTPException(
            status_code=400,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"}
        )
