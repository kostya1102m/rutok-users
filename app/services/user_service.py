from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy import select
from starlette import status
from starlette.responses import JSONResponse


from models.user import UserCreate, UserUpdate
from repository.user_repository import UserRepository
from db.tables import Role

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
        user = await self.repository.get_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")
        return user
    
    async def get_user_by_username(
        self,
        name: str,
        session: AsyncSession
    ):
        user = await self.repository.get_by_username(name, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с логином {name} не найден")
        return user
    
    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession
    ):
        user = await self.repository.get_by_email(email, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с email {email} не найден")
        return user
    
    async def get_user_all(
        self,
        session: AsyncSession
    ):
        return await self.repository.get_all(session)
    
    async def create_user(
        self,
        userCreate: UserCreate,
        session: AsyncSession
    ):
        try:
            role = await session.execute(select(Role).filter(Role.id == userCreate.role_id))
            role = role.scalar_one_or_none()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Роль с id {userCreate.role_id} не найдена"
                )
            existing_user = await self.repository.get_by_email(userCreate.email, session)
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email уже зарегистрирован")
            
            user = await self.repository.create(userCreate, session)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                content={
                    "detail": "Пользователь создан", 
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    }
            )
        
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
        except DataError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.orig))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    async def update_user(
        self,
        id: int,
        userUpdate: UserUpdate,
        session: AsyncSession
    ):
        user = await self.repository.update(id, userUpdate, session)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "detail": "Пользователь обновлен",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    
    async def delete_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        user = await self.repository.delete(id, session)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "detail": "Пользователь удалён",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
    
    async def ban_user_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        user = await self.repository.ban(id, session)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "detail": "Пользователь забанен",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })
        
    




