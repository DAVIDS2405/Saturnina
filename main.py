from app.server import app
from app.database.database import Connection

@app.on_event("startup")
async def startup_event():
    await Connection()







