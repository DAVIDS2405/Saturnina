from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.routers import user_routers


app = FastAPI(
    docs_url="/api/v1/docs",
    title="Saturnina Api",
    description="Api para el e-commerce de la tienda saturnina",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
    redoc_url=None,
    
)   
app.include_router(user_routers.router,prefix="/api/v1")
 

@app.get("/",include_in_schema=False)
async def read_root():
    return RedirectResponse("/api/v1/docs")