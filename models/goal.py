from datetime import date
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Boolean, Column, String, Date, Integer
from database import Base


class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_at = Column(Date, nullable=False)
    end_at = Column(Date, nullable=True)
    achieved = Column(Boolean, nullable=False, default=False)

class CreateGoal(BaseModel):
    title: str
    description: Optional[str] = None
    start_at: date
    end_at: Optional[date] = None
    achieved: bool = False

class UpdateGoal(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_at: Optional[date] = None
    end_at: Optional[date] = None
    achieved: Optional[bool] = None

class GoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    start_at: date
    end_at: Optional[date] = None
    achieved: bool = False

    class Config:
        from_attributes = True