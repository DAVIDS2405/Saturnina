import secrets
import string
import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr

class Email_User(BaseModel):
    email:EmailStr
class User_Recover_Password(BaseModel):
    new_password: SecretStr
    check_password:SecretStr
class User_Login(BaseModel):
    email: EmailStr
    password: SecretStr 
class User_Register(User_Login):
    nombre: str 
    apellido: str 
    telefono: str
    
class User_DB (User_Register):
    status: bool = Field(default= True)
    token: str = Field(default=None)
    confirmEmail: bool =  Field(default=False)
    githubId: int = Field(default=0)
    password_requiered: bool = Field(default= False)
    
    def generate_token(self):
        new_token = string.ascii_letters + string.digits
        new_token = self.token = ''.join(secrets.choice(new_token) for _ in range(36))
        return new_token
    
    def encrypt_password(self) -> str:
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(self.password.get_secret_value().encode('utf-8'), salt)
        return hashed_password        
    
    def verify_password(plain_password,password_bd: str) -> bool:
        return bcrypt.checkpw(plain_password.get_secret_value().encode(),password_bd.encode('utf-8'))
    
   
    


    