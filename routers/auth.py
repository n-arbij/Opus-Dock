from fastapi import APIRouter, Depends, HTTPException, status
from dependency import authenticate_user, create_access_token
from models.user import CreateUser
from database import get_db
from sqlalchemy.orm import Session
from services.userservices import UserService
from pwdlib import PasswordHash
from datetime import datetime, timezone

route = APIRouter(prefix="/auth", tags=["auth"])

hashed_password = PasswordHash.recommended()
def get_password_hash(password):
    return hashed_password.hash(password)


@route.post("/register")
async def register(user: CreateUser, db: Session = Depends(get_db)):
    service = UserService(db)

    existing_user = service.get_user_by_email(user.email)
    if existing_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = service.create_user(
        name = user.name,
        email = user.email,
        hashed_password = hashed_password,
        timezone = user.timezone,
        created_at = datetime.now(timezone.utc)
    )

    return new_user

@route.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(email, password, db)
    if not authenticated_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": authenticated_user.email})
    return {"access_token": access_token, "token_type": "bearer"}