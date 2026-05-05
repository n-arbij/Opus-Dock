from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Event(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    recurring_rule: Optional[str] = None
    color: Optional[str] = None
    all_day: Optional[bool] = False

class CreateEvent(Event):
    user_id: UUID

class UpdateEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    recurring_rule: Optional[str] = None
    color: Optional[str] = None
    all_day: Optional[bool] = None

class EventResponse(Event):
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True