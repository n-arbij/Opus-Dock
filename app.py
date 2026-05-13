from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import get_db
from database import get_db
from services.habitservices import HabitService # type: ignore
from routers import api_router, public_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()
db = get_db()
habit_service = HabitService(db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(
        func = habit_service.create_daily_log,
        trigger = CronTrigger(hour=0, minute=0)
    )
    scheduler.start()

    yield # Application runs here

    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "Welcome to the OpusDoc API"
    }

# Routers
app.include_router(public_router)
app.include_router(api_router)