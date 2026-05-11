from sqlalchemy.orm import Session
from models import User

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, timezone: str = None, created_at=None):
        new_user = User(name=name, email=email, timezone=timezone, created_at=created_at)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def update_user(self, user_id, name=None, email=None, timezone=None):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if timezone is not None:
            user.timezone = timezone
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user