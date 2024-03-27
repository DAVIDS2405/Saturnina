from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from helpers.jwt_helper import decodeJWT
security = HTTPBearer()


async def JWTBearer(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials

    payload = await decodeJWT(token)

    return payload
