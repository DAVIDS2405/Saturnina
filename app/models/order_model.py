from typing import List, Optional
from pydantic import BaseModel, Field

from models.enums.category import Tallas


class Order(BaseModel):
    user_id: str = Field(examples=["user_saturnina:mnr0nnm2kbrjrxor19p4"])
    price_order: float = Field(gt=1, lt=9999, examples=[12.50])
    products: List[Data_product_order] = [{"id_producto": "product:yzr5f0ydfwwwp9luwj0i", "cantidad": 1, "talla": "Talla x", "color": "Amarillo"}, {
        "id_producto": "product:yzr5f0ydfwwwp9luwj0i", "cantidad": 3}] or []
    nombre: str = Field(examples=["David"], min_length=3, max_length=10)
    apellido: str = Field(examples=["Basantes"], min_length=3, max_length=10)
    direccion: str = Field(
        examples=["La magdalena"], min_length=10, max_length=40)
    email: str = Field(examples=["sebastian2405lucero@hotmail.com"])
    telefono: str = Field(examples=["090095964"], min_length=10, max_length=10)
    descripcion: Optional[str] = Field(max_length=100, examples=[
                                       "Me gustaria que fuera de color rojo y el bordado con una letra D"], default="")

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        print(value)
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @field_validator("price_order")
    def validate_precio_decimales(cls, value):
        if value != round(value, 2):
            raise ValueError("El precio debe tener exactamente 2 decimales")
        return value

    @field_validator("nombre")
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es de 3  a 10 caracteres")

        return value

    @field_validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es de 3 a 10 caracteres")

        return value

    @field_validator("telefono")
    def validate_telefono(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "El telefono debe ser unicamente de 10 dígitos y contener solo números")
        return value

    @field_validator("descripcion")
    def validate_direccion(cls, value):
        if len(value) > 100:
            raise ValueError(
                "El comentario no puede ser mayor a 100 caracteres")
        return value


class Update(BaseModel):
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

    @field_validator("nombre", mode='before')
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError(
                "El rango permitido es de 3 a 10 caracteres")

        return value

    @field_validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es de 3 a 10 caracteres")
        return value

    @field_validator("direccion")
    def validate_direccion(cls, value):
        if len(value) < 5 or len(value) > 50:
            raise ValueError(
                "La direccion debe de tener entre 5 a 100 caracteres")
        return value

    @field_validator("telefono")
    def validate_telefono(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "El telefono debe ser unicamente de 10 dígitos y contener solo números")
        return value


class Product(BaseModel):
    id_producto: str
    cantidad: int = Field(gt=0, lt=11)
    talla: Optional[Tallas] = None
    color: Optional[str] = None


class UpdateStatus(BaseModel):
    status_order: Estados_orden
    descripcion: str = Field(max_length=50, min_length=5)

    @validator("descripcion")
    def validate_descripcion(cls, value):
        if len(value) < 5 or len(value) > 50:
            raise ValueError(
                "El comentario debe de tener entre 5 a 100 caracteres")
        return value

    @validator("status_order", pre=True)
    def validate_status_order(cls, value):
        if value not in [estado.value for estado in Estados_orden]:
            raise ValueError(
                f"Estado de orden no válido. Los estados válidos son: {', '.join(e.value for e in Estados_orden)}")
        return value
