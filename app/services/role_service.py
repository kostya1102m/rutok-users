from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from starlette import status
from starlette.responses import JSONResponse


from models.role import RoleCreate
from repository.role_repository import RoleRepository


class RoleService:
    def __init__(
        self,
        repository: RoleRepository
    ):
        self.repository = repository
        
    async def get_role_all(
        self,
        session: AsyncSession
    ):
        return await self.repository.get_all(session)
    
    async def get_role_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        role = await self.repository.get_by_id(id, session)
        return role
    
    async def create_role(
        self,
        roleCreate: RoleCreate,
        session: AsyncSession
    ):
        role = await self.repository.create(roleCreate, session)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "detail": "Роль создана",
            "id": role.id,
            "name": role.role_name,
            "description": role.role_description
        })
    
    async def delete_role(
        self,
        id: int,
        session: AsyncSession
    ):
        role = await self.repository.delete(id, session)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "detail": "Роль удалена",
            "id": role.id,
            "name": role.role_name,
            "description": role.role_description
        })
    
    async def set_user_role(
        self,
        user_id: int,
        role_id: int,
        session: AsyncSession
    ):
        user = await self.repository.set_role(user_id, role_id, session)
        return JSONResponse(status_code=status.HTTP_200_OK, content={
            "detail": f"Роль пользователя {user.username} изменена",
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role_id": user.role_id
        })
    
    
        
    
    




