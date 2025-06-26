from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.responses import JSONResponse
import logging

from app.models.role import RoleCreate
from app.repository.role_repository import RoleRepository


logger = logging.getLogger(__name__)

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
        try:
            logger.info("Получение списка всех ролей")
            roles = await self.repository.get_all(session)
            if roles is None:
                logger.warning("Роли не найдены")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Роли не найдены")
            logger.debug("Получено %d ролей", len(roles))
            return roles
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def get_role_by_id(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Получение роли с id %s", id)
            role = await self.repository.get_by_id(id, session)
            if role is None:
                logger.warning("Роль с id %s не найдена", id)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Роль с id {id} не найдена")
            logger.debug("Получена роль: id=%s, name=%s, description=%s", role.id, role.role_name, role.role_description)
            return role
        
        except HTTPException as e:
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : id=%s", id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def create_role(
        self,
        roleCreate: RoleCreate,
        session: AsyncSession
    ):
        try:
            logger.info("Создание роли")
            role = await self.repository.create(roleCreate, session)
            logger.debug("Роль создана: id=%s, name=%s, description=%s", role.id, role.role_name, role.role_description)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                "detail": "Роль создана",
                "id": role.id,
                "name": role.role_name,
                "description": role.role_description
            })
        
        except HTTPException as e:
            logger.error("Роль с именем %s уже существует", roleCreate.role_name)
            raise e
        
        except ValidationError as e:
            logger.error("Ошибка валидации при создании роли: %s", e.errors())
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def delete_role(
        self,
        id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Удаление роли с id %s", id)
            role = await self.repository.delete(id, session)
            logger.debug("Роль удалена: id=%s, name=%s, description=%s", role.id, role.role_name, role.role_description)
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                "detail": "Роль удалена",
                "id": role.id,
                "name": role.role_name,
                "description": role.role_description
            })
        
        except HTTPException as e:
            raise e
        
        except SQLAlchemyError:
            logger.error("Недопустимое значение : id=%s", id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    async def set_user_role(
        self,
        user_id: int,
        role_id: int,
        session: AsyncSession
    ):
        try:
            logger.info("Изменение роли пользователя с id %s", user_id)
            user = await self.repository.set_role(user_id, role_id, session)
            
            role = await self.repository.get_by_id(role_id, session)
            role_name = role.role_name
            logger.debug("Роль пользователя изменена: id=%s, username=%s, email=%s, role_id=%s, role_name=%s", user.id, user.username, user.email, user.role_id, role_name)
            return JSONResponse(status_code=status.HTTP_200_OK, content={
                "detail": f"Роль пользователя {user.username} изменена",
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role_id": user.role_id
            })
            
        except HTTPException as e:
            raise e
        
        except SQLAlchemyError:
            unexcepted_id = user_id if abs(user_id) > abs(role_id) else role_id
            logger.error("Недопустимое значение : id=%s", unexcepted_id)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недопустимое значение : id={unexcepted_id}")
        
        except Exception as e:
            logger.error("Непредвиденная ошибка сервера: %s", str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
            
    
    
        
    
    




