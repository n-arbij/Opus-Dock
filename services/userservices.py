from sqlalchemy.orm import Session
from database import User
from uuid import UUID


class UserService:
    def __init__ (self, db: Session):
        self.db = db

    def create_user(self, CreateUser):
        new_user = CreateUser(**CreateUser.dict())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update_user(self, user_id: UUID, UpdateUser):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        for key, value in UpdateUser.dict().items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user(self, user_id: UUID):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def delete_user(self, user_id: UUID):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user