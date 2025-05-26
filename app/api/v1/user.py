from fastapi import Depends, APIRouter, Request, Response
from starlette.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.user_service import UserService
from repository.user_repository import UserRepository
from models.user import UserCreate
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"],
)

async def get_user_service():
    user_repository = UserRepository()
    return UserService(user_repository)


@router.get("/")
async def get_users(
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_all(session)

@router.get("/{id}")
async def get_user_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_id(id, session)

@router.get("/email/{email}")
async def get_user_by_email(
    email: str,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_email(email, session)

@router.get("/username/{username}")
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_username(username, session)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    userCreate: UserCreate,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.create_user(userCreate, session)

@router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.delete_user_by_id(id, session)

@router.put("/ban/{id}", status_code=status.HTTP_200_OK)
async def ban_user_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.ban_user_by_id(id, session)