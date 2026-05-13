from pydantic import BaseModel, Field
from typing import Optional
from database import Base
from datetime import date
from sqlalchemy import Column, DateTime, String, Integer, Boolean, Date


class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    target_days = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    color = Column(String, nullable=True)
    achieved = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=date.today)

class HabitCreate(BaseModel):
    user_id: int
    title: str
    target_days: int
    start_date: date
    color: Optional[str] = None
    achieved: bool = False
    created_at: DateTime = Field(default_factory=date.today)

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    target_days: Optional[int] = None
    start_date: Optional[date] = None
    color: Optional[str] = None
    achieved: Optional[bool] = None
    created_at: Optional[DateTime] = None

class HabitResponse(Habit):
    id: int
    user_id: int
    title: str
    target_days: int
    start_date: date
    color: Optional[str] = None
    achieved: bool
    created_at: DateTime

    class Config:
        from_attributes = True