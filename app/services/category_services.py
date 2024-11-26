
from typing import Any, List
import uuid
from interface.repository_interface import RepositoryInterface
from logger.logger import logger
from models import user_model
from helpers.password.users_password import encrypt_password, generate_token
from config.smtp_config import send_email
from prisma import Prisma


class CategoryService (RepositoryInterface):
    def __init__(self, db: Prisma):
        self.db = db

    async def create(self, data: user_model.User) -> None:
        await self.db.connect()
        user = data.model_dump()
        user.update(password=encrypt_password(data.password).decode("utf-8"))
        user.update(token=generate_token())

        try:
            email = send_email(user.get('name'), user.get('token'))
            rol = await self.db.rol.find_unique(where={'type_rol': "User"})
            await self.db.user.create(data={
                'email': user.get('email'),
                'password': user.get('password'),
                'phone': user.get('phone'),
                'name': user.get('name'),
                'last_name': user.get('last_name'),
                'token': user.get('token'),
                'rol': {'connect': {'id': rol.id}}
            })
            await self.db.disconnect()
            return email
        except Exception as error:
            logger.error(f"Unexpected error during user creation: {error}")
            await self.db.disconnect()
            raise error

    async def exists(self, email: str) -> bool:
        await self.db.connect()
        result = await self.db.user.find_unique(where={'email': email})

        await self.db.disconnect()

        return result

    async def update(self, data: Any) -> None:
        await self.db.connect()

        await self.db.user.update(
            where={'id': data.get('id')},
            data={
                'token': "",
                'confirm_email': True
            }
        )

    async def delete(self, email: str) -> None:
        await self.db.delete(id)

    async def get(self) -> List[Any]:
        return super().get()
