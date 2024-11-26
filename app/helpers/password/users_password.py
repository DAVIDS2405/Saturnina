import secrets
import string
import bcrypt
from fastapi import HTTPException, status


def generate_token():
    new_token = string.ascii_letters + string.digits
    new_token = ''.join(secrets.choice(new_token) for _ in range(36))
    return new_token


def encrypt_password(password) -> str:
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(
        password.get_secret_value().encode('utf-8'), salt)
    return hashed_password


def verify_password(plain_password, password_bd: str) -> bool:
    check_pass = bcrypt.checkpw(plain_password.get_secret_value().encode(
        'utf-8'), password_bd.encode('utf-8'))

    if not check_pass:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Your email or password is not correct")
    return check_pass
