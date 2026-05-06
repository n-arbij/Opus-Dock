from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
driver = os.getenv("DB_DRIVER")

params = urllib.parse.quote_plus(
    f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;TrustServerCertificate=yes;"
)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    timezone = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    frequency = Column(String, nullable=False)
    target_count = Column(Integer, nullable=False)
    color = Column(String, nullable=True)
    achieved = Column(Boolean, default=False)
    achieved_today = Column(Boolean, default=False)

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    entry_date = Column(DateTime, nullable=False)
    count = Column(Integer, nullable=False)
    note = Column(String, nullable=True)

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)
    title = Column(String, index=True)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    start_at = Column(Date, nullable=False)
    end_at = Column(Date, nullable=False)
    status = Column(Boolean, default=False)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    recurring_rule = Column(String, nullable=True)
    color = Column(String, nullable=True)
    all_day = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)


Base.metadata.create_all(bind=engine)