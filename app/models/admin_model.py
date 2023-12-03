import json
from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str
    
    
class Products(BaseModel):
    nombre_producto: str = Field(examples=["Reparacion de gorras"])
    id_categoria: str = Field(examples=["category:115pijy2vnwpsioq2iwm"])
    descripcion: str = Field(examples=["Repara tu  gorra con lindos bordados"])
    precio: float  = Field(examples=[22.22])

    
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    

class Order_update_status(BaseModel):
    status_order: str