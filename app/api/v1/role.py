from fastapi import Depends, APIRouter, Request, Response
from starlette.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.role_service import RoleService
from repository.role_repository import RoleRepository
from models.role import RoleCreate
from database import get_db

router = APIRouter(
    prefix="/roles",
    tags=["Role"],
)

async def get_role_service():
    role_repository = RoleRepository()
    return RoleService(role_repository)


@router.get("/")
async def get_roles(
    session: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    return await role_service.get_role_all(session)

@router.get("/{id}")
async def get_role_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    return await role_service.get_role_by_id(id, session)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_role(
    roleCreate: RoleCreate,
    session: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    return await role_service.create_role(roleCreate, session)

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_role_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    return await role_service.delete_role(id, session)

@router.put("/set/{user_id}/{role_id}", status_code=status.HTTP_200_OK)
async def set_user_role(
    user_id: int,
    role_id: int,
    session: AsyncSession = Depends(get_db),
    role_service: RoleService = Depends(get_role_service)
):
    return await role_service.set_user_role(user_id, role_id, session)
