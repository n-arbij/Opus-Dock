import uuid
from pydantic import BaseModel


class Habit(BaseModel):
    id: uuid
    user_id: uuid  
    name: str
    frequency: str
    target_count: int
    color: str
    achieved: bool