import logging
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from starlette import status
from starlette.responses import JSONResponse

from models.user import UserCreate, UserUpdate
from repository.user_repository import UserRepository
from db.tables import Role


logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        logger.info("Получение пользователя с id %s", id)
        user = await self.repository.get_by_id(id, session)
        
        if user is None:
            logger.warning("Пользователь с id %s не найден", id)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")
        
        logger.info("Получен пользователь: id=%s, username=%s", user.id, user.username)
        return user

    async def get_user_by_username(
        self,
        name: str,
        session: AsyncSession
    ):
        logger.info("Получение пользователя с логином %s", name)
        user = await self.repository.get_by_username(name, session)
        
        if user is None:
            logger.warning("Пользователь с логином %s не найден", name)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с логином {name} не найден")
        
        logger.debug("Получен пользователь: id=%s, username=%s", user.id, user.username)
        return user

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession
    ):
        logger.info("Получение пользователя с email %s", email)
        user = await self.repository.get_by_email(email, session)
        
        if user is None:
            logger.warning("Пользователь с email %s не найден", email)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с email {email} не найден")
        
        logger.debug("Получен пользователь: id=%s, email=%s", user.id, user.email)
        return user

    async def get_user_all(
        self,
        session: AsyncSession
    ):
        logger.info("Получение всех пользователей")
        users = await self.repository.get_all(session)
        logger.debug("Получено %d пользователей", len(users))
        return users

    async def create_user(
        self,
        userCreate: UserCreate,
        session: AsyncSession
    ):
        try:
            logger.info("Создание пользователя с email %s", userCreate.email)
            role = await session.execute(select(Role).filter(Role.id == userCreate.role_id))
            role = role.scalar_one_or_none()
            
            if role is None:
                logger.warning("Роль с id %s не найдена при создании пользователя", userCreate.role_id)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Роль с id {userCreate.role_id} не найдена"
                )
            existing_user = await self.repository.get_by_email(userCreate.email, session)
            
            if existing_user:
                logger.warning("Email %s уже зарегистрирован", userCreate.email)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email {userCreate.email} уже зарегистрирован")
            
            user = await self.repository.create(userCreate, session)
            logger.info("Пользователь создан: id=%s, username=%s, email=%s", user.id, user.username, user.email)
            
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "detail": "Пользователь создан",
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            )
            
        except ValidationError as e:
            logger.error("Ошибка валидации при создании пользователя: %s", e.errors())
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=e.errors())
        except SQLAlchemyError as e:
            logger.error("Конфликт данных при создании пользователя: %s", str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str(e))
        except HTTPException as e:
            logger.error('%s', str(e))
            raise e
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def update_user(self, id: int, userUpdate: UserUpdate, session: AsyncSession):
        logger.info("Обновление пользователя с id %s", id)
        user = await self.repository.update(id, userUpdate, session)
        logger.info("Пользователь обновлён: id=%s, username=%s, email=%s", user.id, user.username, user.email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": "Пользователь обновлен",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        )

    async def delete_user_by_id(self, id: int, session: AsyncSession):
        logger.info("Удаление пользователя с id %s", id)
        user = await self.repository.delete(id, session)
        logger.info("Пользователь удалён: id=%s, username=%s, email=%s", user.id, user.username, user.email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": "Пользователь удалён",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        )

    async def ban_user_by_id(self, id: int, session: AsyncSession):
        logger.info("Блокировка пользователя с id %s", id)
        user = await self.repository.ban(id, session)
        logger.info("Пользователь заблокирован: id=%s, username=%s, email=%s", user.id, user.username, user.email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "detail": "Пользователь забанен",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }
        )