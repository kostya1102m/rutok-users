from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.models.user import UserRegister, UserSchema, UserUpdate, UserAuth
from app.database import get_db

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
    user_id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_id(user_id, session)

@router.get("/email/{email}", response_model=UserSchema)
async def get_user_by_email(
    email: str,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_email(email, session)

@router.get("/username/{user_name}", response_model=UserSchema)
async def get_user_by_username(
    user_name: str,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_user_by_username(user_name, session)

@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_register: UserRegister,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.register_user(user_register, session)

@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(
    user_auth: UserAuth,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.authenticate_user(user_auth, session)

@router.patch("/ban/{id}", status_code=status.HTTP_200_OK)
async def ban_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.ban_user_by_id(user_id, session)

@router.patch("/unban/{id}", status_code=status.HTTP_200_OK)
async def unban_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.unban_user_by_id(user_id, session)

@router.patch("/update/{id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.update_user(user_id, user_update, session)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    return await user_service.delete_user_by_id(user_id, session)