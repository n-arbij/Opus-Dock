from datetime import datetime, date, time, timezone
from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Optional
from sqlalchemy import DateTime, Time, Date, Integer, String, Boolean, Column
from database import Base

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    recurring_rule = Column(String, nullable=True)
    color = Column(String, nullable=True)
    all_day = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)


class CreateEvent(BaseModel):
    title: str
    description: Optional[str] = None

    start_date: date
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

    all_day: bool = False

    recurring_rule: Optional[str] = None
    color: Optional[str] = None
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]

@model_validator(mode="after")
def validate_event_logic(self):
    if self.all_day:
        if self.start_time or self.end_time:
            raise ValueError("All-day events cannot have start or end times")
        
    if self.start_date and self.end_date:
        if self.start_date is None and self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")
    
    if self.end_date and self.start_date < self.end_date:
        raise ValueError("Start date must be before end date")
    
    return self
    
    
class UpdateEvent(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    recurring_rule: Optional[str] = None
    color: Optional[str] = None
    all_day: Optional[bool] = None

class EventResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    recurring_rule: Optional[str] = None
    color: Optional[str] = None
    all_day: Optional[bool] = False
    created_at: datetime
    
    class Config:
        from_attributes = True