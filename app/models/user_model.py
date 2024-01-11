from enum import Enum
import json
import secrets
import string
from typing import List, Optional
import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr, validator

class Email_User(BaseModel):
    email:EmailStr

class Recover_Pass(BaseModel):
    email:EmailStr
    token: str = Field(default=None)
    def generate_token(self):
        new_token = string.ascii_letters + string.digits
        new_token = self.token = ''.join(secrets.choice(new_token) for _ in range(36))
        return new_token
class User_Recover_Password(BaseModel):
    new_password: SecretStr = Field(min_length=9, max_length=18)
    check_password:SecretStr = Field(min_length=9,max_length=18)
    
    def encrypt_password(self) -> str:
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(self.new_password.get_secret_value().encode('utf-8'), salt)
        bcrypt.hashpw(self.check_password.get_secret_value().encode('utf-8'), salt)
        return hashed_password  
    
    def verify_password(plain_password,password_bd: str) -> bool:
        return bcrypt.checkpw(plain_password.get_secret_value().encode(),password_bd.encode('utf-8'))
    
    @validator("new_password")
    def validate_new_password(cls, value):
        raw_password = value.get_secret_value()

        if not any(char.isupper() for char in raw_password):
            raise ValueError(
                "La contraseña debe contener al menos una letra mayúscula")

        if not any(char.isdigit() for char in raw_password):
            raise ValueError("La contraseña debe contener al menos un número")

        special_chars = "!@#$%^&*()-_+=<>?/[]{}|"
        if not any(char in special_chars for char in raw_password):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial")
            
        if len(raw_password) < 9 or len (raw_password) > 18:
            raise ValueError(
                "La contraseña debe tener 9 o 18 caracteres unicamente")

        return value
    
    
class User_Login(BaseModel):
    email: EmailStr
    password: SecretStr 
    
    @validator("email", pre=True)
    def check_email(cls,value):
        if value is None:
            raise ValueError("Ingresa un correo")
        return value
            
    
class User_Register(BaseModel):
    email: EmailStr
    password: SecretStr
    nombre: str = Field(min_length=3, max_length=10)
    apellido: str = Field(min_length=3, max_length=10)
    telefono: str = Field(min_length=10, max_length=10)
    
    @validator("nombre",pre=True)
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es menor a 3 o mayor a 10 caracteres")
        
        return value
    
    @validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es menor a 3 o mayor a 10")
        
        return value

    @validator("telefono")
    def validate_telefono(cls, value):
        if len(value) != 10:
            raise ValueError("El telefono debe de ser unicamente de 10 digitos")
        return value
    
    @validator("password")
    def validate_password(cls, value):
        raw_password = value.get_secret_value()

        if not any(char.isupper() for char in raw_password):
            raise ValueError(
                "La contraseña debe contener al menos una letra mayúscula")

        if not any(char.isdigit() for char in raw_password):
            raise ValueError("La contraseña debe contener al menos un número")

        special_chars = "!@#$%^&*()-_+=<>?/[]{}|"
        if not any(char in special_chars for char in raw_password):
            raise ValueError(
                "La contraseña debe contener al menos un carácter especial")

        if len(raw_password) < 9 or len(raw_password) > 18:
            raise ValueError(
                "La contraseña debe tener 9 o 18 caracteres unicamente")

        return value
    
    @validator("email", pre=True)
    def check_email(cls,value):
        if value is None:
            raise ValueError("Ingresa un correo")
        return value

class User_Update(BaseModel):
    nombre: str = Field(min_length=3, max_length=10)
    apellido: str = Field(min_length=3, max_length=10)
    telefono: str = Field(min_length=10, max_length=10)

    @validator("nombre", pre=True)
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError(
                "El rango permitido es menor a 3 o mayor a 10 caracteres")

        return value

    @validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es menor a 3 o mayor a 10")

        return value

    @validator("telefono")
    def validate_telefono(cls, value):
        if len(value) != 10:
            raise ValueError(
                "El telefono debe de ser unicamente de 10 digitos")
        return value
class User_DB (User_Register):
    status: bool = Field(default= True)
    token: str = Field(default=None)
    confirmEmail: bool =  Field(default=False)

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

class Tallas(str,Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
class Data_product_order(BaseModel):
    id_producto: str 
    cantidad: int
    talla: Optional[Tallas] = None
    color: Optional[str] = None
    

class Order(BaseModel):
    user_id: str = Field(examples=["user_saturnina:mnr0nnm2kbrjrxor19p4"])
    price_order: float = Field(gt=1, lt=500, examples=[12.50])
    products: List[Data_product_order] = [{"id_producto": "product:yzr5f0ydfwwwp9luwj0i", "cantidad": 1, "talla":"Talla x","color": "Amarillo"}, {"id_producto": "product:yzr5f0ydfwwwp9luwj0i", "cantidad": 3}] or []
    nombre: str = Field(examples=["David"], min_length=3, max_length=10)
    apellido: str = Field(examples=["Basantes"], min_length=3, max_length=10)
    direccion: str = Field(
        examples=["La magdalena"], min_length=10, max_length=40)
    email: str = Field(examples=["sebastian2405lucero@hotmail.com"])
    telefono: str = Field(examples=["090095964"], min_length=10, max_length=10)
    descripcion: Optional[str] = Field( max_length=100,examples=["Me gustaria que fuera de color rojo y el bordado con una letra D"],default="")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    @validator("price_order")
    def validate_precio_decimales(cls, value):
        if value != round(value, 2):
            raise ValueError("El precio debe tener exactamente 2 decimales")
        return value
    
    @validator("nombre")
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es menor a 3 o mayor a 10 caracteres")
        
        return value
    
    @validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es menor a 3 o mayor a 10")
        
        return value

    @validator("telefono")
    def validate_telefono(cls, value):
        if len(value) != 10:
            raise ValueError("El telefono debe de ser unicamente de 10 digitos")
        return value

    @validator("descripcion")
    def validate_direccion(cls,value):
        if len(value) > 100:
            raise ValueError ("El comentario debe de tener entre 100 caracteres")
        return value

    
class Order_update(BaseModel):
    nombre: str = Field(examples=["David"], min_length=3, max_length=10)
    apellido: str = Field(examples=["Basantes"], min_length=3, max_length=10)
    direccion: str = Field(
        examples=["La magdalena"], min_length=10, max_length=40)
    email: str = Field(examples=["sebastian2405lucero@hotmail.com"])
    telefono: str = Field(examples=["090095964"], min_length=10, max_length=10)
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value   

    @validator("nombre", pre=True)
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError(
                "El rango permitido es menor a 3 o mayor a 10 caracteres")

        return value

    @validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es menor a 3 o mayor a 10")
        return value
    @validator("direccion")
    def validate_direccion(cls, value):
        if len(value) < 5 or len(value) >50:
            raise ValueError(
                "La direccion debe de tener entre 5 a 100 caracteres")
        return value



class Comment_product(BaseModel):
    descripcion: Optional[str] = Field(min_length=10, max_length=100)
    id_producto: str
    calificacion: int = Field(gt=0, le=5) 
    user_id :str
    
    @validator("descripcion")
    def validate_descripcion(cls, value):
        if len(value) < 10 or len(value) > 100:
            raise ValueError ("El comentario debe de tener entre 10 a 100 caracteres")
        return value
