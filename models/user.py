from pydantic import BaseModel
from datetime import datetime
import uuid


class User (BaseModel):
    id: uuid
    name: str
    email: str
    timezone: str
    created_at: datetime

