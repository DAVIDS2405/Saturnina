from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, UTC
from config.index import settings

ALGORITHM = settings.ALGORITHM
SECRET_KEY = settings.SECRET_KEY


def create_token(data: dict):

    access_token_expires = timedelta(minutes=30)

    expire = datetime.now(UTC) + access_token_expires

    access_token = {"user_id": data, "exp": expire}
    JWT = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    return JWT


def validate_token(token: str):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El Token ha expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def verify_rol(token: str, required_role: str = 'User'):

    payload = validate_token(token)

    if payload["rol"] != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para acceder a este recurso."
        )

    return payload["user_id"]
