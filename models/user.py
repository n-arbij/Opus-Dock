from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    timezone = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=False)

class CreateUser(BaseModel):
    name: str
    email: str
    timezone: Optional[str] = None
    created_at: datetime

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    timezone: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    timezone: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True