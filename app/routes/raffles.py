from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.db import get_db
from app.models import Raffle,Ticket,StockEntry,EntryLedger
from app.schemas import Raffle as RaffleSchema
from app.crud import get_active_raffle
from app.deps import get_current_user

from fastapi.responses import JSONResponse



router = APIRouter(
    prefix="/api/raffles",  # ✅ This ensures all routes are under /api/raffles
    tags=["raffles"]
)

@router.get("/current", response_model=Optional[RaffleSchema])
async def get_current_raffle():
    """Get the currently active raffle"""
    
    
    db = next(get_db())
    raffle = get_active_raffle(db)
    if raffle:
        return {
            "id": raffle.id,
            "title": raffle.title,
            "headline_prize": raffle.headline_prize,
            "month_key": raffle.month_key
        }
    return {"message": "No active raffle found"}

@router.get("/active")
def get_active_raffles(db: Session = Depends(get_db)):
    """
    Public endpoint.
    Fetch the currently active raffle where is_active=True.
    Returns a simple dict or None if no active raffle is found.
    """
    raffle = (
        db.query(Raffle)
        .filter(Raffle.is_active == True)
        .first()
    )

    if not raffle:
        return {"message": "No active raffle found"}

    # Manually convert SQLAlchemy object to dict
    return {
            "id": raffle.id,
            "title": raffle.title,
            "headline_prize": raffle.headline_prize,
            "month_key": raffle.month_key
        }

@router.post("/join")
def join_active_raffle(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # 1️⃣ Get the active raffle (SQLAlchemy object!)
        raffle = get_active_raffle(db)
        if not raffle:
            raise HTTPException(status_code=404, detail="No active raffle found")

        # 2️⃣ Get user's available entries
        stock_entry = db.query(StockEntry).filter_by(user_id=current_user.id).first()
        if not stock_entry or stock_entry.balance <= 0:
            raise HTTPException(status_code=400, detail="You have no entries to spend")

        entries_to_use = stock_entry.balance

        # 3️⃣ Create tickets
        tickets = []
        for _ in range(entries_to_use):
            ticket = Ticket(
                user_id=current_user.id,
                raffle_id=raffle.id,
                created_at=datetime.utcnow()
            )
            db.add(ticket)
            tickets.append(ticket)

        # 4️⃣ Log in EntryLedger
        ledger_entry = EntryLedger(
            user_id=current_user.id,
            raffle_id=raffle.id,
            source="Spent",
            amount=entries_to_use,
            status="spent"
        )
        db.add(ledger_entry)

        # 5️⃣ Deduct all entries from stock
        stock_entry.balance = 0

        # 6️⃣ Commit changes
        db.commit()

        return {
            "message": f"Successfully joined the raffle using all {entries_to_use} entries",
            "raffle": {
                "id": raffle.id,
                "title": raffle.title,
                "headline_prize": raffle.headline_prize,
                "month_key": raffle.month_key
            },
            "tickets_created": len(tickets),
            "remaining_entries": stock_entry.balance
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})