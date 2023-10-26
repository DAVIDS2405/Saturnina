from surrealdb import Surreal
from dotenv import load_dotenv
from fastapi import HTTPException
import os 

load_dotenv()
url_db = os.getenv("URL_DB")
username_db = os.getenv("USER_DB")
password_db = os.getenv("PASSWORD_DB")
namespace_db = os.getenv("NAMESPACE_DB")
database_db = os.getenv("DATABASE_DB")

async def Connection():
    try:
        conn = Surreal()
        await conn.connect("wss://suturnina-db.fly.dev")
        await conn.signin({"user": f"{username_db}", "pass": f"{password_db}"})
        await conn.use(f"{namespace_db}", f"{database_db}")
        return conn
    except Exception as e:
        print("Ocurrió un error con surreal:", str(e))
        await conn.close(),
        raise ( HTTPException(status_code= 502,detail={"error":str(e)}))
