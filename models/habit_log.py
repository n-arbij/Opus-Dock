from pydantic import BaseModel
from datetime import date
# from typing import Optional
from sqlalchemy import Boolean, String, Column, Integer, DateTime
from database import Base


class HabitLog(Base):
    __tablename__ = "habit_logs"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, nullable=False)
    entry_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)

class CreateHabitLog(BaseModel):
    habit_id: int
    entry_date: date
    completed: bool = False

# class UpdateHabitLog(BaseModel):
#     entry_date: Optional[date] = None
#     completed: Optional[bool] = None

class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    entry_date: DateTime
    completed: bool = False

    class Config:
        from_attributes = True
