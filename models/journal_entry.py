from sqlalchemy import Column, Integer, String, DateTime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from database import Base
from typing import Optional


class JournalEntry(Base):
    __tablename__ = 'journal_entries'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    body = Column(String, nullable=False)
    mood = Column(String, nullable=False)
    entry_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True)

class CreateJournalEntry(BaseModel):
    body: str
    mood: str
    entry_date: datetime

class UpdateJournalEntry(BaseModel):
    body: Optional[str] = None
    mood: Optional[str] = None
    update_date: datetime

class JournalEntryResponse(BaseModel):
    id: int
    user_id: int
    body: str
    mood: str
    entry_date: datetime
    update_date: datetime

    class Config:
        from_attributes = True