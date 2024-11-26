from typing import Optional
from pydantic import BaseModel, Field


class Comment_product(BaseModel):
    descripcion: Optional[str] = Field(min_length=10, max_length=100)
    id_producto: str
    calificacion: int = Field(gt=0, le=5)
    user_id: str

    @field_validator("descripcion")
    def validate_descripcion(cls, value):
        if len(value) < 10 or len(value) > 100:
            raise ValueError(
                "El comentario debe de tener entre 10 a 100 caracteres")
        return value


class Comment_general(BaseModel):
    descripcion: Optional[str] = Field(min_length=10, max_length=100)
    calificacion: int = Field(gt=0, le=5)
    user_id: str

    @field_validator("descripcion")
    def validate_descripcion(cls, value):
        if len(value) < 10 or len(value) > 100:
            raise ValueError(
                "El comentario debe de tener entre 10 a 100 caracteres")
        return value
