from fastapi import APIRouter, HTTPException, Response, status, Request
from authlib.integrations.starlette_client import OAuthError
from helpers.auth.JWT import create_token
from helpers.auth.authlib_google import oauth
from fastapi.responses import RedirectResponse
router = APIRouter(
    tags=["External Auth"]
)


@router.get("/login-google")
async def google_User_Session(request: Request):
    redirect_uri = request.url_for('google_callback')  # function name
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response


@router.get("/google/logout")
async def google_User_Session_Logout(request: Request, response: Response):
    request.session.pop('token')
    return HTTPException(status_code=status.HTTP_202_ACCEPTED, detail={"Cierre de session"})


@router.get("/auth/google/callback")
async def google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)

    except OAuthError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "msg": "Algo salio mal intenta de nuevo"})
    user = token.get('userinfo')
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "user not found"})
    JWT = create_token(data=dict(user))

    request.session['token'] = JWT

    return RedirectResponse("http://localhost:4321/")
