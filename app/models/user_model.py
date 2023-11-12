import json
import secrets
import string
from typing import List
import bcrypt
from fastapi import Body
from pydantic import BaseModel, EmailStr, Field, SecretStr

class Email_User(BaseModel):
    email:EmailStr
class User_Recover_Password(BaseModel):
    new_password: SecretStr
    check_password:SecretStr
    
    def encrypt_password(self) -> str:
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(self.new_password.get_secret_value().encode('utf-8'), salt)
        bcrypt.hashpw(self.check_password.get_secret_value().encode('utf-8'), salt)
        return hashed_password  
    
    def verify_password(plain_password,password_bd: str) -> bool:
        return bcrypt.checkpw(plain_password.get_secret_value().encode(),password_bd.encode('utf-8'))
class User_Login(BaseModel):
    email: EmailStr
    password: SecretStr 
class User_Register(User_Login):
    nombre: str 
    apellido: str 
    telefono: str

class User_Update(BaseModel):
    nombre:str
    apellido:str
    telefono:str
    email:str
class User_DB (User_Register):
    status: bool = Field(default= True)
    token: str = Field(default=None)
    confirmEmail: bool =  Field(default=False)
    # githubId: int = Field(default=0)
    # password_requiered: bool = Field(default= False)
    
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
    
class Data_product_order(BaseModel):
    id_producto: str 
    cantidad: int
    

class Order(BaseModel):
    user_id: str = Field(examples=["user_saturnina:mnr0nnm2kbrjrxor19p4"])
    price_order: float = Field(gt=0)
    products: List[Data_product_order] = [{"id_producto":"ni idea","cantidad":1},{"id_producto":"123213","cantidad":3}]
    nombre: str = Field(examples=["David"])
    apellido: str = Field(examples=["Basantes"])
    direccion: str = Field(examples=["La magdalena"])
    email: str = Field(examples=["sebastian2405lucero@hotmail.com"])
    telefono: str = Field(examples=["090095964"])
    descripcion: str = Field(examples=["Me gustaria que fuera de color rojo y el bordado con una letra D"])

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    
class Order_update(BaseModel):
    nombre: str = Field(examples=["David"])
    apellido: str = Field(examples=["Basantes"])
    direccion: str = Field(examples=["La magdalena"])
    email: str = Field(examples=["sebastian2405lucero@hotmail.com"])
    telefono: str = Field(examples=["090095964"])
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value   


    