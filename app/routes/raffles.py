# app/routes/raffles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.db import get_db
from app.models import Raffle
from app.schemas import Raffle as RaffleSchema

router = APIRouter(prefix="/api/raffles", tags=["raffles"])


@router.get("/current", response_model=Optional[RaffleSchema])
def get_current_raffle(db: Session = Depends(get_db)):
    """
    Get the currently active raffle.
    A raffle is considered active if today's date is within its start and end.
    """
    now = datetime.utcnow()

    raffle = (
        db.query(Raffle)
        .filter(Raffle.start_date <= now, Raffle.end_date >= now)
        .order_by(Raffle.start_date.desc())
        .first()
    )

    if not raffle:
        raise HTTPException(status_code=404, detail="No active raffle found")

    return raffle
