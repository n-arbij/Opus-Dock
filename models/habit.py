from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class Habit(BaseModel):
    name: str
    frequency: str
    target_count: int
    color: Optional[str] = None

class HabitCreate(Habit):
    user_id: UUID

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    frequency: Optional[str] = None
    target_count: Optional[int] = None
    color: Optional[str] = None
    achieved: Optional[bool] = None

class HabitResponse(Habit):
    id: UUID
    user_id: UUID
    achieved: bool
    achieved_today: Optional[bool] = None

    class Config:
        from_attributes = True