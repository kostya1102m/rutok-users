from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from starlette import status
from datetime import datetime

from app.models.user import UserCreate, UserUpdate
from app.db.tables import User


class UserRepository:
    
    
    async def get_item(
        self,
        attribute_name: str,
        attribute_value: str,
        session: AsyncSession
    ):
        result = await session.execute(select(User).where(getattr(User, attribute_name) == attribute_value))
        return result.scalars().first()
    
    async def get_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        return await self.get_item("id", id, session)

    async def get_by_username(
        self,
        name: str,
        session: AsyncSession
    ):
        return await self.get_item("username", name, session)
    
    async def get_by_email(
        self,
        email: str,
        session: AsyncSession
    ):
        return await self.get_item("email", email, session)

    async def get_all(
        self,
        session: AsyncSession
    ):
        result = await session.execute(select(User))
        return result.scalars().all()

    async def create(
        self,
        userCreate: UserCreate,
        session: AsyncSession
    ):
        try:
            new_user = User(**userCreate.model_dump())
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Пользователь с email {userCreate.email} уже зарегистрирован")
    
    async def update(
        self,
        id: int,
        userUpdate: UserUpdate,
        session: AsyncSession
    ):
        user = await self.get_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")    
        update_data = userUpdate.model_dump(exclude_unset=True)
        
        if "email" in update_data:
            existing_user = await self.get_by_email(update_data["email"], session)
            if existing_user and existing_user.id != id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот email уже занят")
        
        for key, value in update_data.items():
            setattr(user, key, value)
            
        user.updated_at = datetime.now()
        await session.commit()
        await session.refresh(user)
        return user
        
    
    async def delete(
        self,
        id: int,
        session: AsyncSession
    ):
        user = await self.get_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")
        await session.delete(user)
        await session.commit()
        return user
    
    async def ban(
        self,
        id: int,
        session: AsyncSession
    ):
        user = await self.get_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")
        user.banned = True
        await session.commit()
        return user
    
    async def unban(
        self,
        id: int,
        session: AsyncSession
    ):
        user = await self.get_by_id(id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {id} не найден")
        user.banned = False
        await session.commit()
        return user
