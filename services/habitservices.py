from models.habit import Habit, HabitCreate, HabitUpdate, HabitResponse
from models.habit_log import HabitLog
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, timedelta, timezone, datetime

class HabitService:
    def __init__(self, db: Session):
        self.db = db

    def create_habit(self, habit_create: HabitCreate) -> HabitResponse:
        habit = Habit(
            user_id=habit_create.user_id,
            title=habit_create.title,
            target_days=habit_create.target_days,
            color=habit_create.color,
            achieved=habit_create.achieved
        )
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return HabitResponse.from_orm(habit)
    
    def create_daily_log(self, user_id: int) -> dict:
        today = date.today()
        created_count = 0
        skipped_count = 0

        active_habits = self.get_active_habits(user_id, today)

        for habit in active_habits:
            existing_log = self.db.query(HabitLog).filter(
                HabitLog.habit_id == habit.id,
                HabitLog.entry_date == today
            ).first()

            if existing_log:
                skipped_count += 1
                continue

            new_log = HabitLog(
                habit_id=habit.id,
                entry_date=today,
                completed=False
            )
            self.db.add(new_log)
            created_count += 1

        return {
            "date": today,
            "logs_created": created_count,
            "logs_skipped": skipped_count,
        }

    def get_habits(self, user_id: int) -> List[HabitResponse]:
        habits = self.db.query(Habit).filter(Habit.user_id == user_id).all()
        return [HabitResponse.from_orm(habit) for habit in habits]
    
    def get_active_habits(self, user_id: int, today: date) -> List[HabitResponse]:
        all_habits = self.get_habits(user_id)
        return [
            habit for habit in all_habits
            if habit.start_date <= today <= habit.start_date + timedelta(days=habit.target_days - 1) and not habit.achieved
        ]

    def get_habit(self, habit_id: int) -> Optional[HabitResponse]:
        habit = self.db.query(Habit).filter(Habit.id == habit_id).first()
        if habit:
            return HabitResponse.from_orm(habit)
        return None
    
    def get_progress(self, habit_id: int) -> dict:
        habit = self.get_habit(habit_id)
        if not habit:
            return {"error": "Habit not found"}

        completed_logs = self.db.query(HabitLog).filter(
            HabitLog.habit_id == habit_id,
            HabitLog.completed == True
        ).count()

        days_elapsed = (habit.created_at.date() - habit.start_date).days + 1

        end_date = habit.start_date + timedelta(days=habit.target_days - 1)
        if date.today() > end_date:
            days_elapsed = (end_date - habit.start_date).days + 1
        total_logs = self.db.query(HabitLog).filter(HabitLog.habit_id == habit_id).count()
        is_completed = completed_logs >= habit.target_days
        
        progress_percentage = (completed_logs / habit.target_days) * 100 if habit.target_days > 0 else 0
        return {
            "title": habit.title,
            "target_days": habit.target_days,
            "days_completed": completed_logs,
            "days_elapsed": days_elapsed,
            "total_logs": total_logs,
            "progress_percentage": progress_percentage,
            "is_completed": is_completed
        }
    
    def is_habit_achieved(self, habit_id: int) -> bool:
        habit = self.get_habit(habit_id)
        if not habit:
            return False
        
        completed_logs = self.db.query(HabitLog).filter(
            HabitLog.habit_id == habit_id,
            HabitLog.completed == True
        ).count()

        return completed_logs >= habit.target_days
    
    def tick_habit(self, habit_id: int) -> Optional[HabitResponse]:
        today = date.today()
        
        log = self.db.query(HabitLog).filter(
            HabitLog.habit_id == habit_id,
            HabitLog.entry_date == today
        ).first()

        if not log:
            raise ValueError("No log entry found for today. Daily log may not have been created yet.")
        if log.completed:
            raise ValueError("Today's habit have been ticked.")
        
        log.completed = True
        log.logged_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(log)
        return log

    def update_habit(self, habit_id: int, habit_update: HabitUpdate) -> Optional[HabitResponse]:
        habit = self.db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            return None
        
        habit.title = habit_update.title or habit.title
        habit.target_days = habit_update.target_days or habit.target_days
        habit.color = habit_update.color or habit.color
        habit.achieved = habit_update.achieved if habit_update.achieved is not None else habit.achieved

        self.db.commit()
        self.db.refresh(habit)
        return HabitResponse.from_orm(habit)

    def delete_habit(self, habit_id: int) -> bool:
        habit = self.db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            return False
        self.db.delete(habit)
        self.db.commit()
        return True