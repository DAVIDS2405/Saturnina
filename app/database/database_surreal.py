from dotenv import load_dotenv
from surrealdb import Surreal, SurrealHTTP
import os

load_dotenv()

url_db = os.environ.get("URL_DB")
username_db = os.environ.get("USER_DB")
password_db = os.environ.get("PASSWORD_DB")
namespace_db = os.environ.get("NAMESPACE_DB")
database_db = os.environ.get("DATABASE_DB")


async def Connection():
    try:
        conn = SurrealHTTP(
            url_db,
            namespace_db,
            database_db,
            username_db,
            password_db
        )

        return conn

    except Exception as e:

        print(e)

        return None
