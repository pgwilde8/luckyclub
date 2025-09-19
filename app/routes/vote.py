from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func   # 👈 ADD THIS
from app.db import get_db
from app.crud import create_user, authenticate_user, get_user_by_email
from app.models import User, Vote
from app.schemas import VoteCreate, VoteResponse
from app.crud import save_vote
from app.deps import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/votes/", response_model=VoteResponse)
def create_vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 👈 here
):

   # check for existing vote
    existing_vote = db.query(Vote).filter(
        Vote.user_id == current_user.id,
        Vote.year == vote.year,
        Vote.month == vote.month
    ).first()

    if existing_vote:
        raise HTTPException(
            status_code=400,
            detail=f"You has already voted for {vote.month}/{vote.year}"
        )
    # use current_user.id instead of passing user_id from frontend
    new_vote = save_vote(
        db=db,
        user_id=current_user.id,
        year=vote.year,
        month=vote.month,
        prize_name=vote.prize_name,
        amount=2
    )
    return new_vote

@router.get("/votes/results")
def get_poll_results(db: Session = Depends(get_db)):
    now = datetime.now()
    year, month = now.year, now.month

    # ✅ predefined prize list
    prize_options = [
        "Gaming Laptop",
        "Smartphone",
        "Cash Prize",
        "Vacation Package"
    ]

    # query existing votes
    results = (
        db.query(Vote.prize_name, func.count(Vote.vote_id).label("count"))
        .filter(Vote.year == year, Vote.month == month)
        .group_by(Vote.prize_name)
        .all()
    )

    # convert to dict for easy lookup
    votes_dict = {r.prize_name: r.count for r in results}

    # ensure all prizes are included (even if 0 votes)
    poll_results = [
        {"prize_name": prize, "count": votes_dict.get(prize, 0)}
        for prize in prize_options
    ]

    return {"year": year, "month": month, "results": poll_results}