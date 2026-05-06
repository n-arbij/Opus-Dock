from datetime import date
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class Goal(BaseModel):
    title: str
    description: Optional[str] = None
    start_at: date
    end_at: date
    status: bool

class CreateGoal(Goal):
    pass

class UpdateGoal(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_at: Optional[date] = None
    end_at: Optional[date] = None
    status: Optional[bool] = None

class GoalResponse(Goal):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True