import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from starlette import status
from starlette.responses import JSONResponse

from app.models.user import UserCreate, UserRegister, UserUpdate, UserAuth
from app.repository.user_repository import UserRepository
from app.repository.role_repository import RoleRepository
from app.db.tables import Role
import app.utils as utils


logger = logging.getLogger(__name__)

class UserService:
    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    async def get_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Получение пользователя с id %s", id)
            user = await self.repository.get_by_id(id, session)
            if user is None:
                logger.warning("Пользователь с id %s не найден", id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")
            
            logger.debug("Получен пользователь: id=%s, user_name=%s", user.id, user.user_name)
            return user
        
        except HTTPException as e:
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : id=%s", id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

    async def get_user_by_username(
        self,
        name: str,
        session: AsyncSession
    ):
        try:
            logger.info("Получение пользователя с user_name %s", name)
            user = await self.repository.get_by_username(name, session)
            if user is None:
                logger.warning("Пользователь с user_name %s не найден", name)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с username {name} не найден")
            
            logger.debug("Получен пользователь: id=%s, user_name=%s", user.id, user.user_name)
            return user
        
        except HTTPException as e:
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : username=%s", name)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : username={name}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession
    ):
        try:
            logger.info("Получение пользователя с email %s", email)
            user = await self.repository.get_by_email(email, session)
            if user is None:
                logger.warning("Пользователь с email %s не найден", email)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с email {email} не найден")
            
            logger.debug("Получен пользователь: id=%s, username=%s", user.id, user.user_name)
            return user
        
        except HTTPException as e:
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : email=%s", email)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : email={email}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_user_all(
        self,
        session: AsyncSession
    ):
        try:
            logger.info("Получение списка всех пользователей")
            users = await self.repository.get_all(session)
            if users is None:
                logger.warning("Пользователи не найдены")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователи не найдены")
            logger.debug("Получено %d пользователей", len(users))
            return users
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def register_user(
        self,
        user_register: UserRegister,
        session: AsyncSession
    ):
        try:
            logger.info("Создание пользователя с email %s", user_register.email)
            
            #pwd = user_register.password
            #hashed_pwd = utils.hash_password(pwd) выпилено, сразу получаю хэш

            default_user_role = await RoleRepository().get_by_name("USER", session)
            default_user_role_id = default_user_role.id

            
            user_create = UserCreate(
                user_name=user_register.user_name,
                email=user_register.email,
                hash_password=user_register.hashed_password,
                role_id=default_user_role_id
            )
            
            # role = await session.execute(select(Role).filter(Role.id == user_create.role_id))
            # role = role.scalar_one_or_none()
            
            # if role is None:
            #     logger.warning("Роль с id %s не найдена при создании пользователя", user_create.role_id)
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail=f"Роль с id {user_create.role_id} не найдена"
            #     )
            
            user = await self.repository.create(user_create, session)
            logger.info("Пользователь создан: id=%s, username=%s, email=%s", user.id, user.user_name, user.email)
            
            
            return user.id
        
        except HTTPException as e:
            logger.error('%s', e.detail)
            raise e
        
        except SQLAlchemyError as e:
            logger.error("Ошибка данных при регистрации пользователя: %s", str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str(e))
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def update_user(
        self,
        id: int,
        userUpdate: UserUpdate,
        session: AsyncSession
    ):
        try:
            logger.info("Обновление информации пользователя с id %s", id)
            user = await self.repository.update(id, userUpdate, session)
            logger.info("Информация обновлена: id=%s, username=%s, email=%s", user.id, user.user_name, user.email)
        
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Информация обновлена",
                    "user": {
                        "userId": user.id,
                        "userName": user.user_name,
                        "email": user.email,
                        "phone": user.phone,
                        "bio": user.bio
                    }
                }
            )
        
        except HTTPException as e:
            logger.warning('%s', e.detail)
            raise e
        
        except SQLAlchemyError as e:
            logger.error("Ошибка данных при обновлении пользователя: %s", str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str(e))
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    
    async def delete_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Удаление пользователя с id %s", id)
            user = await self.repository.delete(id, session)
            logger.info("Пользователь удалён: id=%s, username=%s, email=%s", user.id, user.user_name, user.email)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Пользователь удалён",
                    "user": {
                        "userId": user.id,
                        "userName": user.user_name,
                        "email": user.email
                    }
                }
            )
            
        except HTTPException as e:
            logger.warning('%s', e.detail)
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : id=%s", id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        

    async def ban_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Блокировка пользователя с id %s", id)
            user = await self.repository.ban(id, session)
            logger.info("Пользователь заблокирован: id=%s, username=%s, email=%s", user.id, user.user_name, user.email)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Пользователь забанен",
                    "user": {
                        "userId": user.id,
                        "userName": user.user_name,
                        "email": user.email
                    }
                }
            )
            

        except HTTPException as e:
            logger.warning('%s', e.detail)
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : id=%s", id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
        
    async def unban_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Разблокировка пользователя с id %s", id)
            user = await self.repository.unban(id, session)
            logger.info("Пользователь разблокирован: id=%s, username=%s, email=%s", user.id, user.user_name, user.email)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Пользователь разбанен",
                    "user": {
                        "userId": user.id,
                        "userName": user.user_name,
                        "email": user.email
                    }
                }
            )
            
        except HTTPException as e:
            logger.warning('%s', e.detail)
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : id=%s", id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
        
        
    async def authenticate_user(
        self,
        user_auth: UserAuth,
        session: AsyncSession
    ):
        try:
            logger.info('Аутентификация пользователя %s', user_auth.email)
            user = await self.repository.get_by_email(user_auth.email, session)
            if user is None:
                logger.warning("Пользователь с email %s не найден", user_auth.email)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с email {user_auth.email} не найден")
            
            if not utils.validate_password(user_auth.hashed_password, user.hash_password):
                logger.error("Неверный пароль пользователя с email %s", user_auth.email)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Неверный пароль пользователя с email {user_auth.email}")
            
            if user.banned:
                logger.warning("Пользователь с email %s заблокирован", user_auth.email)
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Пользователь с email {user_auth.email} заблокирован")
            
            logger.info("Пользователь аутентифицирован: id=%s, user_name=%s, email=%s", user.id, user.user_name, user.email)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "detail": "Пользователь аутентифицирован",
                    "user": {
                        "userId": user.id,
                        "userName": user.user_name,
                        "email": user.email
                    }
                }
            )
               
        except HTTPException as e:
            logger.warning('%s', e.detail)
            raise e
        
        except SQLAlchemyError as e:
            logger.error("Ошибка данных при обновлении пользователя: %s", str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str(e))
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))