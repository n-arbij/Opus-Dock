import uuid
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import text


class Event(BaseModel):
    id: uuid
    user_id: uuid
    title: str
    description: text
    start_time: datetime
    end_time: datetime
    recurring_rule: str
    color: str
    all_day: bool