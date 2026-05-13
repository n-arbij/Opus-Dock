from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from dependency import get_current_user_id
from models.goal import CreateGoal, GoalResponse, UpdateGoal
from sqlalchemy.orm import Session
from services.goalservices import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("/", response_model=GoalResponse)
async def create_goal(goal: CreateGoal, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    service = GoalService(db)
    return service.create_goal(
        goal_data = goal,
        current_user_id = current_user_id
    )

@router.get("/", response_model=list[GoalResponse])
async def get_goals(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return db.query(GoalResponse).filter(GoalResponse.user_id == current_user_id).all()

@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: int, db: Session = Depends(get_db)):
    service = GoalService(db)
    goal = service.get_goal_by_id(goal_id)

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return goal

@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(goal_id: int, goal_data: UpdateGoal, db: Session = Depends(get_db)):
    service = GoalService(db)

    try:
        goal = service.update_goal(
            goal_id = goal_id,
            goal_data = goal_data
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Goal not found")

    return goal

@router.delete("/{goal_id}", response_model=GoalResponse)
async def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    service = GoalService(db)

    try:
        goal = service.delete_goal(goal_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Goal not found")

    return goal