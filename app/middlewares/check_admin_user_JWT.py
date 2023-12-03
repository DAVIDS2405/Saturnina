from fastapi import HTTPException,status
from database.database import Connection
from helpers.jwt_helper import decodeJWT


async def Check_rol_user(token:str):
    UserDb = await Connection()
    
    decode_token = await decodeJWT(token)
  
    check_user_db = await UserDb.select(decode_token[0].get("user_id"))
    
    if not check_user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "msg": "El usuario dentro del token no existe"})
    if not decode_token:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "msg": "Necesitas de un token valido para continuar"})
    print(check_user_db["rol"])
    print(decode_token[0].get("rol"))
    if check_user_db["rol"] != decode_token[0].get("rol") and decode_token[0].get("rol") != "rol:74rvq7jatzo6ac19mc79":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
                            "msg": "No tienes acceso a este endopoint necesitas un rol correcto"})
    
    