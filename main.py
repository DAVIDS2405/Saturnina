#imports
from app.server import app
from dotenv import load_dotenv
import uvicorn
import os

# Environment Variables
load_dotenv()


#class main
if __name__ == "__main__":

    host = os.getenv("HOST")
    port = os.getenv("PORT")

    uvicorn.run(app, host=host, port=port)
