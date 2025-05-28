from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from services.user_service import UserService
from repository.user_repository import UserRepository
from models.user import UserRegister, UserSchema
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"],
)

async def get_user_service():
    user_repository = UserRepository()
    return UserService(user_repository)


@router.get("/", response_model=list[UserSchema])
async def get_users(
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_all(session)

@router.get("/{id}", response_model=UserSchema)
async def get_user_by_id(
    id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_id(id, session)

@router.get("/email/{email}", response_model=UserSchema)
async def get_user_by_email(
    email: str,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_email(email, session)

@router.get("/username/{username}", response_model=UserSchema)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_username(username, session)

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(
    userRegister: UserRegister,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.register_user(userRegister, session)

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