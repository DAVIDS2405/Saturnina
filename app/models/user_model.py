import bcrypt
from pydantic import BaseModel

class User_Data(BaseModel):
    username: str
    password: str
    
def encrypt_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)    
    
