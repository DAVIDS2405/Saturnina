from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routers import user_routers


app = FastAPI(
    docs_url="/api/v1/docs",
    title="Saturnina Api",
    description="Api para el e-commerce de la tienda saturnina",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
    redoc_url=None,
    
)   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Puedes restringir los métodos específicos (e.g., ["GET", "POST"])
    allow_headers=["*"],  # Puedes restringir los encabezados específicos
)
app.include_router(user_routers.router,prefix="/api/v1")

@app.get("/",include_in_schema=False)
async def read_root():
    return RedirectResponse("/api/v1/docs")

