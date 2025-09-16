from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.db import get_db
from app.models import Raffle
from app.schemas import Raffle as RaffleSchema
from app.crud import get_active_raffle

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
def get_active_raffle(db: Session = Depends(get_db)):
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