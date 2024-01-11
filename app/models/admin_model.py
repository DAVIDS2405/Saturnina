from decimal import Decimal
from enum import Enum
from typing import List, Optional
import json
from pydantic import BaseModel, Field, validator


class Category(BaseModel):
    name: str = Field(max_length=30, min_length=5)
    @validator("name",pre=True)
    def validate_name(cls,value):
        if len(value) < 5 or len(value) > 30:
            raise ValueError("La categoría necesita tener entre 5 a 30 caracteres")
        
        return value

class Tallas(str, Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    
class tallas_productos(BaseModel):
    name:Tallas
    status: bool   

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    @validator("name")
    def validate_tallas_enum(cls, value):
        tallas_validas = [t.name for t in Tallas]
        for talla in value:
            if talla['name'] not in tallas_validas:
                raise ValueError(f"Talla no válida. Las tallas válidas son: {', '.join(tallas_validas)}")
        return value
    

class colores_productos(BaseModel):
    name:str
    status: bool 

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    
    
class Products(BaseModel):
    nombre_producto: str = Field(examples=["Reparación de gorras"],max_length= 25, min_length=5)
    id_categoria: str = Field(examples=["category:115pijy2vnwpsioq2iwm"])
    descripcion: str = Field(examples=["Repara tu  gorra con lindos bordados"],max_length=50,min_length=5)
    precio: float = Field(examples=[22.22], gt=1, lt=500)
    tallas: Optional[List[tallas_productos]] = [
        {"name": "S", "status": True}, {"name": "S", "status": True}] 
    colores: Optional[List[colores_productos]] = [
        {"name": "verde", "status": True}, {"name": "morado", "status": True}]
    
    
    @validator("nombre_producto", pre=True)
    def validate_nombre_producto(cls, value):
        if len(value) < 5 or len(value) > 25:
            raise ValueError("El rango permitido es de 5 a 25 caracteres")
        
        return value
    
    @validator("descripcion")
    def validate_descripcion(cls, value):
        if len(value) > 50 or len(value) < 5:
            raise ValueError(
                "El comentario debe de tener entre 5 a 50 caracteres")
        return value
    
    @validator("precio")
    def validate_precio_decimales(cls, value):
        if value != round(value, 2):
            raise ValueError("El precio debe tener exactamente 2 decimales")
        return value
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    


    
class Estados_orden(str,Enum):
    P = "Pendiente"
    R = "Rechazado"
    En = "En entrega" 
    F = "Finalizado"
class Order_update_status(BaseModel):
    status_order: Estados_orden
    descripcion: str = Field(max_length=50,min_length=5)
    
    @validator("descripcion")
    def validate_descripcion(cls, value):
        if len(value) < 5 or len(value) > 50:
            raise ValueError ("El comentario debe de tener entre 5 a 100 caracteres")
        return value
    
    @validator("status_order",pre=True)
    def validate_status_order(cls, value):
        if value not in [estado.value for estado in Estados_orden]:
            raise ValueError(f"Estado de orden no válido. Los estados válidos son: {', '.join(e.value for e in Estados_orden)}")
        return value
