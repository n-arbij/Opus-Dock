from fastapi import APIRouter, Depends
from routers import auth, user as user_router
from routers import journal_entry as journal_entry_router
from routers import event as event_router
from routers import goal as goal_router
from dependency import get_current_user

api_router = APIRouter(dependencies=[Depends(get_current_user)])
public_router = APIRouter()

public_router.include_router(auth.route)

api_router.include_router(user_router.route)
api_router.include_router(journal_entry_router.router)
api_router.include_router(event_router.route)
api_router.include_router(goal_router.router)

__all__ = ["api_router"]