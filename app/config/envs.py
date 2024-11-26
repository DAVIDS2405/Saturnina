from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class EnvVars(BaseModel):
    ALGORITHM: str
    SECRET_KEY: str
    GOOGLE_ID: str
    GOOGLE_SECRET: str
    LOGGER_TOKEN: str
    HOST: str
    PORT: str
    EMAIL_HOST: str
    EMAIL_HOST_USER: str
    EMAIL_HOST_PORT: int
    EMAIL_HOST_PASSWORD: str
    API_VERSION: str


settings = EnvVars(

    ALGORITHM=os.getenv("ALGORITHM"),
    SECRET_KEY=os.getenv("SECRET_KEY"),
    GOOGLE_ID=os.getenv("GOOGLE_ID"),
    GOOGLE_SECRET=os.getenv("GOOGLE_SECRET"),
    LOGGER_TOKEN=os.getenv("LOGGER_TOKEN"),
    HOST=os.getenv("HOST"),
    PORT=os.getenv("PORT"),
    EMAIL_HOST=os.getenv("EMAIL_HOST"),
    EMAIL_HOST_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD"),
    EMAIL_HOST_PORT=os.getenv("EMAIL_HOST_PORT"),
    EMAIL_HOST_USER=os.getenv("EMAIL_HOST_USER"),
    API_VERSION=os.getenv("API_VERSION")
)
