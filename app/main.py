import uvicorn
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    # Environment Variables
    load_dotenv()
    host = os.getenv("HOST")  # Host configuration
    port = int(os.getenv("PORT"))   # Port configuration
    uvicorn.run("server:app", host=str(host), port=int(port), reload=True)









