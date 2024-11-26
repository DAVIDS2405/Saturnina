from fastapi import Request, HTTPException, status
from helpers.auth.JWT import validate_token, verify_rol


async def JWTBearerCookie(request: Request, required_role: str = 'User'):

    token = request.session.get('token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You need a token")

    payload = validate_token(token)

    verify_rol(token, required_role)

    return payload
