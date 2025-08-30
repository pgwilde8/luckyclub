from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.crud import create_entry_ledger_entry, get_user_entries_for_raffle, get_active_raffle
from app.schemas import EntryLedgerCreate, EntryLedger
from app.deps import get_current_user
from app.models import User

router = APIRouter()

@router.post("/", response_model=EntryLedger)
def create_user_entry(
    entry: EntryLedgerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new entry ledger entry for the current user"""
    return create_entry_ledger_entry(db=db, entry=entry, user_id=current_user.id)

@router.get("/", response_model=List[EntryLedger])
def read_user_entries(
    raffle_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all entries for a specific raffle for the current user"""
    entries = get_user_entries_for_raffle(db, user_id=current_user.id, raffle_id=raffle_id)
    return entries[skip:skip+limit]

@router.get("/summary")
def get_user_entries_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a summary of user entries by source for the currently active raffle"""
    from app.crud import get_user_entries_summary, get_active_raffle
    
    active_raffle = get_active_raffle(db)
    if not active_raffle:
        return []
    
    summary = get_user_entries_summary(db, user_id=current_user.id, raffle_id=active_raffle.id)
    
    # Convert to the format expected by the dashboard
    entries = []
    if summary['base'] > 0:
        entries.append({
            "source": "base",
            "amount": summary['base'],
            "description": "Base monthly entries"
        })
    if summary['vote'] > 0:
        entries.append({
            "source": "vote",
            "amount": summary['vote'],
            "description": "Voting participation entries"
        })
    if summary['share'] > 0:
        entries.append({
            "source": "share",
            "amount": summary['share'],
            "description": "Social sharing entries"
        })
    if summary['upload'] > 0:
        entries.append({
            "source": "upload",
            "amount": summary['upload'],
            "description": "Proof upload entries"
        })
    
    return entries

@router.get("/current-raffle")
def get_current_raffle_entries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get entries for the currently active raffle"""
    active_raffle = get_active_raffle(db)
    if not active_raffle:
        raise HTTPException(status_code=404, detail="No active raffle found")
    
    entries = get_user_entries_for_raffle(db, user_id=current_user.id, raffle_id=active_raffle.id)
    summary = get_user_entries_summary(db, user_id=current_user.id, raffle_id=active_raffle.id)
    
    return {
        "raffle": {
            "id": active_raffle.id,
            "title": active_raffle.title,
            "month_key": active_raffle.month_key
        },
        "entries": entries,
        "summary": summary
    }
