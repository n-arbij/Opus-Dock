from models.journal_entry import CreateJournalEntry, JournalEntry, JournalEntryResponse
from sqlalchemy.orm import Session

class JournalEntryService:
    def __init__(self, db: Session):
        self.db = db


    def create_journal_entry(self, journal_entry: CreateJournalEntry):
        new_entry = JournalEntry(
            user_id=journal_entry.user_id,
            body=journal_entry.body,
            mood=journal_entry.mood,
            entry_date=journal_entry.entry_date
        )
        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)

        return new_entry
    
    def get_journal_entry_by_id(self, entry_id: int):
        return self.db.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    
    def update_journal_entry(self, entry_id: int, body: str = None, mood: str = None, update_date=None):
        entry = self.get_journal_entry_by_id(entry_id)
        if body is not None:
            body = entry.body
        if mood is not None:
            mood = entry.mood    
        update_date = update_date if update_date else entry.update_date

        entry.body = body
        entry.mood = mood
        entry.update_date = update_date
        self.db.commit()
        self.db.refresh(entry)
        
        return entry
    
    def delete_journal_entry(self, id: int):
        entry = self.get_journal_entry_by_id(id)
        if not entry:
            return None
        self.db.delete(entry)
        self.db.commit()
        
        return entry
