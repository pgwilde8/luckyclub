from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.db import get_db
from app.models import Raffle
from app.schemas import Raffle as RaffleSchema

router = APIRouter(
    prefix="/api/raffles",  # ✅ This ensures all routes are under /api/raffles
    tags=["raffles"]
)

# @router.get("/current", response_model=Optional[RaffleSchema])
# def get_current_raffle(db: Session = Depends(get_db)):
#     """Get raffle where today's date is between start/end date"""
#     now = datetime.utcnow()
#     raffle = (
#         db.query(Raffle)
#         .filter(Raffle.start_date <= now, Raffle.end_date >= now)
#         .order_by(Raffle.start_date.desc())
#         .first()
#     )
#     if not raffle:
#         raise HTTPException(status_code=404, detail="No active raffle found")
#     return raffle

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