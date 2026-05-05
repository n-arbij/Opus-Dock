import uuid
from pydantic import BaseModel
from sqlalchemy import text
import datetime


class Journal_entry(BaseModel):
    id: uuid
    user_id: uuid
    entry_date: datetime
    body: text
    mood: str
    mood_score: int
    