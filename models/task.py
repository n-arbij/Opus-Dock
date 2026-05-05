from datetime import date, datetime
from pydantic import BaseModel
import uuid


class Task(BaseModel):
    id: uuid
    user_id: uuid
    goal_id: uuid
    title: str
    due_date: date
    completed: bool
    completed_at: datetime