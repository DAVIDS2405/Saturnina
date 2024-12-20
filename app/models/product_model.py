from typing import Optional
from pydantic import BaseModel, Field

from models.enums.category import Tallas


class Sizes(BaseModel):
    name: Tallas
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
                raise ValueError(
                    f"Talla no válida. Las tallas válidas son: {', '.join(tallas_validas)}")
        return value


class Colors(BaseModel):
    name: str = Field(min_length=5, max_length=10)
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
    nombre_producto: str = Field(
        examples=["Reparación de gorras"], max_length=25, min_length=5)
    id_categoria: str = Field(examples=["category:115pijy2vnwpsioq2iwm"])
    descripcion: str = Field(
        examples=["Repara tu  gorra con lindos bordados"], max_length=50, min_length=5)
    precio: float = Field(examples=[22.22], gt=0, lt=1000)
    tallas: Optional[List[tallas_productos]] = None
    colores: Optional[List[colores_productos]] = None

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
