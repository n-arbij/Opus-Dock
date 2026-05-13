from models.event import CreateEvent, Event, UpdateEvent, EventResponse



class EventService:
    def __init__(self, db):
        self.db = db

    def create_event(self, event_data: CreateEvent, current_user_id: int):
        new_event = Event(
            user_id=current_user_id,
            title=event_data.title,
            description=event_data.description,
            start_date=event_data.start_date,
            end_date=event_data.end_date,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            recurring_rule=event_data.recurring_rule,
            color=event_data.color,
            all_day=False if event_data.start_time and event_data.end_time else True,
            created_at=event_data.created_at
        )
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)

        return new_event
    
    def get_event_by_id(self, event_id):
        return self.db.query(Event).filter(Event.id == event_id).first()
    
    def update_event(self, event_id, event_data: UpdateEvent):
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        
        event.title = event_data.title or event.title
        event.description = event_data.description or event.description
        event.start_date = event_data.start_date or event.start_date
        event.end_date = event_data.end_date or event.end_date
        event.start_time = event_data.start_time or event.start_time
        event.end_time = event_data.end_time or event.end_time
        event.recurring_rule = event_data.recurring_rule or event.recurring_rule
        event.color = event_data.color or event.color
        event.all_day = event_data.all_day if event_data.all_day is not None else event.all_day
        
        self.db.commit()
        self.db.refresh(event)
        
        return event
    
    def delete_event(self, event_id):
        event = self.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        
        self.db.delete(event)
        self.db.commit()
        
        return event