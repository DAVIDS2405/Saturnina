from authlib.integrations.starlette_client import OAuth
from config.envs import settings

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=settings.GOOGLE_ID,
    client_secret=settings.GOOGLE_SECRET,
    client_kwargs={
        'scope': 'openid email profile',
    }
)
