from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from starlette import status
from typing import Sequence

from app.models.role import RoleCreate
from app.repository.user_repository import UserRepository
from app.db.tables import Role

class RoleRepository:

    async def create(
        self,
        roleCreate: RoleCreate,
        session: AsyncSession
    ):
        try:
            new_role = Role(**roleCreate.model_dump())
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)
            return new_role
        
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Роль с именем {roleCreate.role_name} уже существует")

    async def get_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        result = await session.execute(select(Role).where(Role.id == id))
        role = result.scalars().first()
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль с id {id} не найдена")
        return role
    
    async def get_by_name(
        self,
        name: str,
        session: AsyncSession
    ):
        result = await session.execute(select(Role).where(Role.role_name == name))
        role = result.scalars().first()
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль с именем {name} не найдена")
        return role
    
    async def delete(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            result = await session.execute(select(Role).where(Role.id == id))
            role = result.scalars().first()
            if role is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль с id {id} не найдена")
            await session.delete(role)
            await session.commit()
            return role
        
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Роль распределена пользователям и не может быть удалена")
    
    async def get_all(
        self,
        session: AsyncSession
    )  -> Sequence[Role]:
        result = await session.execute(select(Role))
        return result.scalars().all()
    
    async def set_role(
        self,
        user_id: int,
        role_id: int,
        session: AsyncSession
    ):
        user = await UserRepository().get_by_id(user_id, session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {user_id} не найден")
        role = self.get_by_id(role_id, session)
        if role is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль с id {role_id} не найдена")
        user.role_id = role_id
        await session.commit()
        await session.refresh(user)
        return user
    
    
    