from fastapi import APIRouter, Depends
from database import get_db
from models.user import CreateUser, UserResponse, UpdateUser
from uuid import UUID
from services.userservices import UserService
from sqlalchemy.orm import Session
from datetime import datetime, timezone


route = APIRouter(prefix="/users", tags=["users"])

@route.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user: UpdateUser, db: Session = Depends(get_db)):
    service = UserService(db)

    user = service.update_user(
        user_id = user_id,
        name = user.name,
        email = user.email,
        password = user.password,
        timezone = user.timezone
    )

    if not user:
        return {"error": "User not found"}
    
    return user

@route.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user_by_id(user_id)

    if not user:
        return {"error": "User not found"}
    
    return user

@route.delete("/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.delete_user(user_id)

    if not user:
        return {"error": "User not found"}
    
    return {"message": "User deleted successfully"}