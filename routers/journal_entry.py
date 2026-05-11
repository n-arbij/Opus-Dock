from fastapi import APIRouter, Depends
from database import get_db
from models.journal_entry import CreateJournalEntry, JournalEntryResponse, UpdateJournalEntry
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from services.journal_entryservice import JournalEntryService

router = APIRouter(prefix="/journal_entries", tags=["journal_entries"])

@router.post("/", response_model=JournalEntryResponse)
async def create_journal_entry(jornal_entry: CreateJournalEntry, db: Session = Depends(get_db)):
    service = JournalEntryService(db)
    return service.create_journal_entry(
        user_id = jornal_entry.user_id,
        body = jornal_entry.body,
        mood = jornal_entry.mood,
        entry_date = datetime.now(timezone.utc)
    )

@router.get("/{entry_id}", response_model=JournalEntryResponse)
async def get_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    service = JournalEntryService(db)
    entry = service.get_journal_entry_by_id(entry_id)

    if not entry:
        return {"error": "Journal entry not found"}
    
    return entry

@router.put("/{entry_id}", response_model=JournalEntryResponse)
async def update_journal_entry(entry_id: int, journal_entry: UpdateJournalEntry, db: Session = Depends(get_db)):
    service = JournalEntryService(db)

    entry = service.update_journal_entry(
        entry_id = entry_id,
        body = journal_entry.body,
        mood = journal_entry.mood,
        update_date = datetime.now(timezone.utc)
    )

    if not entry:
        return {"error": "Journal entry not found"}
    
    return entry

@router.delete("/{entry_id}", response_model=JournalEntryResponse)
async def delete_journal_entry(entry_id: int, db: Session = Depends(get_db)):
    service = JournalEntryService(db)
    entry = service.delete_journal_entry(entry_id)

    if not entry:
        return {"error": "Journal entry not found"}
    
    return entry