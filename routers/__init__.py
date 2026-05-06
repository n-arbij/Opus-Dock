from fastapi import APIRouter
from routers import user as user_router

api_router = APIRouter()

api_router.include_router(user_router.route)

__all__ = ["api_router"]