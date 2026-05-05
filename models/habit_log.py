import uuid
from pydantic import BaseModel
from sqlalchemy import text
import datetime


class Habit_log(BaseModel):
    id: uuid
    habit_id: uuid
    entry_date: datetime
    count: int
    note: text