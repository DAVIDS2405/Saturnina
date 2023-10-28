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
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg":"Esquema autenticacion invalido."})
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg":"Token invalido o expirado"})
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"msg":"Token invalido o expirado"})

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid