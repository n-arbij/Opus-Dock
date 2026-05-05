from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class JournalEntry(BaseModel):
    body: str
    mood: str
    entry_date: datetime
    
class CreateJournalEntry(JournalEntry):
    user_id: UUID

class UpdateJournalEntry(JournalEntry):
    body: Optional[str] = None
    mood: Optional[str] = None

class JournalEntryResponse(JournalEntry):
    id: UUID
    user_id: UUID
    update_date: datetime

    class Config:
        from_attributes = True