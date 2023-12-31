#The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from helpers.jwt_helper import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg":"Esquema autenticación invalido."})
            payload = await self.verify_jwt(credentials.credentials)
            if payload[0] is False:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "Token inválido o expirado"})
            if payload[1] is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg": "Token inválido o expirado"})
            return credentials.credentials,payload[1]
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg":"Token invalido o expirado"})

    async def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        payload = None
        try:
            payload = await decodeJWT(jwtoken)
            
        except:
            payload = None

        if payload:
            isTokenValid = True
        return (isTokenValid,payload)