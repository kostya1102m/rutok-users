from pydantic import BaseModel, EmailStr, Field
from typing import Optional



class RoleCreate(BaseModel):
    id: int
    role_name : str = Field(..., min_length=2, max_length=10)
    role_description: Optional[str]
    
