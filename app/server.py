from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routers import user_routers, admin_routers, auth_routers, category_routers, orders_routers, payments_routers, products_routers, comments_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from middlewares.Logger import logger_middleware
from config.envs import settings

app = FastAPI(
    docs_url="/api/v1/docs",
    title="Saturnina Api",
    description="Api para el e-commerce de la tienda saturnina",
    version="1.0",
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    redoc_url=None
)


app.add_middleware(BaseHTTPMiddleware, dispatch=logger_middleware)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY,
                   https_only=True, same_site='strict')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routers.router, prefix=settings.API_VERSION)
app.include_router(user_routers.router, prefix=settings.API_VERSION)
app.include_router(admin_routers.router, prefix=settings.API_VERSION)
app.include_router(comments_router.router, prefix=settings.API_VERSION)
app.include_router(payments_routers.router, prefix=settings.API_VERSION)
app.include_router(products_routers.router, prefix=settings.API_VERSION)
app.include_router(category_routers.router, prefix=settings.API_VERSION)


@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse(f"{settings.API_VERSION}/docs")


@app.get("/health_check")
async def health_check():
    return "Servers Run"
