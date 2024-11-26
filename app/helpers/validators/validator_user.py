from pydantic import EmailStr, SecretStr


def validate_first_name(value: str) -> str:
    if len(value) < 3 or len(value) > 10:
        raise ValueError("The length must be between 3 and 10 characters.")
    return value


def validate_last_name(value: str) -> str:
    if len(value) < 3 or len(value) > 10:
        raise ValueError("The length must be between 3 and 10 characters.")
    return value


def validate_phone(value: str) -> str:
    if not value.isdigit() or len(value) != 10:
        raise ValueError(
            "The phone number must contain exactly 10 digits and only numbers.")
    return value


def validate_password(value: SecretStr) -> SecretStr:
    raw_password = value.get_secret_value()

    if not any(char.isupper() for char in raw_password):
        raise ValueError(
            "The password must contain at least one uppercase letter.")

    if not any(char.isdigit() for char in raw_password):
        raise ValueError("The password must contain at least one number.")

    special_chars = "!@#$%^&*()-_+=<>?/[]{}|"
    if not any(char in special_chars for char in raw_password):
        raise ValueError(
            "The password must contain at least one special character.")

    if len(raw_password) < 9 or len(raw_password) > 18:
        raise ValueError(
            "The password must be exactly 9 to 18 characters long.")

    return value


def validate_email(value: EmailStr) -> EmailStr:
    if value is None:
        raise ValueError("Please provide an email address.")
    return value
