from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.deps import get_current_user
from app.models import StockEntry, EntryLedger, Raffle,Ticket,ProofUpload
import traceback

router = APIRouter()

@router.get("/dashboard")
async def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Get user dashboard data with stock balance and detailed entry stats"""
    try:
        # 1️⃣ Get current active raffle
        raffle = db.query(Raffle).filter(Raffle.is_active == True).first()
        if raffle:
            raffle_data = {
                "id": raffle.id,
                "title": getattr(raffle, "title", None),
                "headline_prize": getattr(raffle, "headline_prize", None),
                "month_key": getattr(raffle, "month_key", None)
            }

            # 2️⃣ Calculate entries by source for this raffle and user
            entries_query = (
                db.query(
                    EntryLedger.source,
                    func.sum(EntryLedger.amount).label("total")
                )
                .filter(
                    EntryLedger.user_id == current_user.id,
                    EntryLedger.raffle_id == raffle.id
                )
                .group_by(EntryLedger.source)
                .all()
            )

            # Convert query result to dictionary with defaults
            user_stats = {
                "base_entries": 0,
                "vote_entries": 0,
                "share_entries": 0,
                "upload_entries": 0,
                "total_entries": 0
            }

            for row in entries_query:
                key = f"{row.source}_entries"
                if key in user_stats:
                    user_stats[key] = row.total
                    user_stats["total_entries"] += row.total

        else:
            raffle_data = None
            user_stats = {
                "base_entries": 0,
                "vote_entries": 0,
                "share_entries": 0,
                "upload_entries": 0,
                "total_entries": 0
            }

        # 3️⃣ Get user's stock balance
        stock_entry = db.query(StockEntry).filter_by(user_id=current_user.id).first()
        user_balance = stock_entry.balance if stock_entry else 0

         # 4 Get user's tickets balance
        tickets = db.query(Ticket).filter(
            Ticket.user_id == current_user.id,
            Ticket.raffle_id ==raffle.id
        ).count()

        # 5 Pending proofs
        pending_proofs = db.query(ProofUpload).filter(
            ProofUpload.user_id == current_user.id,
            ProofUpload.raffle_id ==raffle.id,
            ProofUpload.status == "pending"
        ).count()

        return {
            "current_raffle": raffle_data,
            "stock_balance": user_balance,
            "user_stats": user_stats,
            "pending_proofs": pending_proofs,
            "tickets": tickets
        }

    except Exception as e:
        # Print traceback to console for debugging
        traceback.print_exc()
        # Return 500 error with message
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
