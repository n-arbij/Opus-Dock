from fastapi import APIRouter
from routers import user as user_router
from routers import journal_entry as journal_entry_router

api_router = APIRouter()

api_router.include_router(user_router.route)
api_router.include_router(journal_entry_router.router)

__all__ = ["api_router"]