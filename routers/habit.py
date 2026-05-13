from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.habit import HabitCreate, HabitUpdate, HabitResponse
from services.habitservices import HabitService
from database import get_db
from typing import List
from fastapi import HTTPException


router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("/", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    return habit_service.create_habit(habit)

@router.post("/daily")
def create_daily_habits(db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    return habit_service.create_daily_habits()

@router.get("/active", response_model=List[HabitResponse])
def get_active_habits(db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    return habit_service.get_active_habits()

@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    habit = habit_service.get_habit_by_id(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.get("/", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    return habit_service.get_habits()

@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, habit_update: HabitUpdate, db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    habit = habit_service.update_habit(habit_id, habit_update)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.delete("/{habit_id}", response_model=HabitResponse)
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit_service = HabitService(db)
    habit = habit_service.delete_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit