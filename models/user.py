from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional


class User (BaseModel):
    name: str
    email: EmailStr
    timezone: Optional[str] = None


class CreateUser (User):
    pass

class UpdateUser (BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    timezone: Optional[str] = None

class UserResponse (User):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True