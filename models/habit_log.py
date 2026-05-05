from uuid import UUID
from pydantic import BaseModel
from datetime import date
from typing import Optional


class HabitLog(BaseModel):
    entry_date: date
    count: int
    note: Optional[str] = None

class CreateHabitLog(HabitLog):
    habit_id: UUID

class UpdateHabitLog(BaseModel):
    entry_date: Optional[date] = None
    count: Optional[int] = None
    note: Optional[str] = None

class HabitLogResponse(HabitLog):
    id: UUID
    habit_id: UUID
    
    class Config:
        from_attributes = True
