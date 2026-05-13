from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from database import get_db
from dependency import get_current_user
from models.event import CreateEvent, EventResponse, UpdateEvent
from sqlalchemy.orm import Session

from services.eventservice import EventService

route = APIRouter(prefix="/events", tags=["events"])

@route.post("/")
async def create_event(event: CreateEvent, current_user_id = Depends(get_current_user), db: Session = Depends(get_db)):
    service = EventService(db)
    return service.create_event(
        event_data = event,
        current_user_id = current_user_id
        )

@route.get("/")
async def get_events(db: Session = Depends(get_db)):
    return db.query(EventResponse).filter(EventResponse.user_id == get_current_user()).all()

@route.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventResponse).filter(EventResponse.id == event_id).first()
    if not event:
        return {"error": "Event not found"}
    return event

@route.put("/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, event_data: UpdateEvent, db: Session = Depends(get_db)):
    event = db.query(EventResponse).filter(EventResponse.id == event_id).first()
    if not event:
        return {"error": "Event not found"}
    
    event.title = event_data.title or event.title
    event.description = event_data.description or event.description
    event.event_date = event_data.event_date or event.event_date
    event.start_time = event_data.start_time or event.start_time
    event.end_time = event_data.end_time or event.end_time
    event.recurring_rule = event_data.recurring_rule or event.recurring_rule
    event.color = event_data.color or event.color
    event.all_day = event_data.all_day if event_data.all_day is not None else event.all_day
    
    db.commit()
    db.refresh(event)
    
    return event

@route.delete("/{event_id}", response_model=EventResponse)
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(EventResponse).filter(EventResponse.id == event_id).first()
    if not event:
        return {"error": "Event not found"}
    
    db.delete(event)
    db.commit()
    
    return event