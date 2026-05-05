from datetime import date, datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class Task(BaseModel):
    title: str
    due_date: Optional[date] = None

class TaskCreate(Task):
    user_id: UUID
    goal_id: Optional[UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None

class TaskResponse(Task):
    id: UUID
    user_id: UUID
    goal_id: Optional[UUID] = None
    completed: bool
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True