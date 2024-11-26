import secrets
import string
import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator
from helpers.validators.validator_user import validate_first_name, validate_last_name, validate_password, validate_phone, validate_email


class Email_User(BaseModel):
    email: EmailStr


class RecoverPasswordEmail(BaseModel):
    email: EmailStr
    token: str = Field(default=None)

    def generate_token(self):
        new_token = string.ascii_letters + string.digits
        new_token = self.token = ''.join(
            secrets.choice(new_token) for _ in range(36))
        return new_token


class RecoverPassword(BaseModel):
    new_password: SecretStr = Field(min_length=9, max_length=18)
    check_password: SecretStr = Field(min_length=9, max_length=18)

    def encrypt_password(self) -> str:
        salt = bcrypt.gensalt(10)
        hashed_password = bcrypt.hashpw(
            self.new_password.get_secret_value().encode('utf-8'), salt)
        bcrypt.hashpw(
            self.check_password.get_secret_value().encode('utf-8'), salt)
        return hashed_password

    def verify_password(plain_password, password_bd: str) -> bool:
        return bcrypt.checkpw(plain_password.get_secret_value().encode(), password_bd.encode('utf-8'))

    @field_validator("new_password")
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

        if len(raw_password) < 9 or len(raw_password) > 18:
            raise ValueError(
                "La contraseña debe tener 9 o 18 caracteres unicamente")

        return value


class Login(BaseModel):
    email: EmailStr
    password: SecretStr

    @field_validator("email", mode='before')
    def check_email(cls, value):
        if value is None:
            raise ValueError("Ingresa un correo")
        return value


class User(BaseModel):
    email: EmailStr
    password: SecretStr
    name: str = Field(min_length=3, max_length=10)
    last_name: str = Field(min_length=3, max_length=10)
    phone: str = Field(min_length=10, max_length=10)

    @field_validator("name", mode="before")
    def validate_first_name(cls, value):
        return validate_first_name(value)

    @field_validator("last_name")
    def validate_last_name(cls, value):
        return validate_last_name(value)

    @field_validator("phone")
    def validate_phone(cls, value):
        return validate_phone(value)

    @field_validator("password")
    def validate_password(cls, value):
        return validate_password(value)

    @field_validator("email", mode="before")
    def validate_email(cls, value):
        return validate_email(value)


class UserUpdate(BaseModel):
    nombre: str = Field(min_length=3, max_length=10)
    apellido: str = Field(min_length=3, max_length=10)
    telefono: str = Field(min_length=10, max_length=10)
    email: EmailStr

    @field_validator("nombre", mode='before')
    def validate_nombre(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError(
                "El rango permitido es de 3  10 caracteres")

        return value

    @field_validator("apellido")
    def validate_apellido(cls, value):
        if len(value) < 3 or len(value) > 10:
            raise ValueError("El rango permitido es de 3 o mayor a 10")

        return value

    @field_validator("telefono")
    def validate_telefono(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError(
                "El telefono debe ser unicamente de 10 dígitos y contener solo números")
        return value
