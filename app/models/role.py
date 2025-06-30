from pydantic import Field
from typing import Optional
from app.models.user import BaseSchema



class RoleCreate(BaseSchema):
    id: int
    role_name : str = Field(..., min_length=2, max_length=10)
    role_description: Optional[str]
    
