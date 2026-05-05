from datetime import date
import uuid
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text


class Goal(BaseModel):
    id: uuid
    user_id: uuid
    title: str
    description: Optional[text] = None
    start_at: date
    end_at: date
    status: bool