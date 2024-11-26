
class Category(BaseModel):
    name: str = Field(max_length=30, min_length=5)

    @validator("name", pre=True)
    def validate_name(cls, value):
        if len(value) < 5 or len(value) > 30:
            raise ValueError(
                "La categoría necesita tener entre 5 a 30 caracteres")

        return value
    

