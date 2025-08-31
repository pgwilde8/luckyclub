from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
#from datetime import datetime

from app.db import get_db
from app.crud import (
    create_raffle, get_all_raffles, get_pending_proofs, review_proof,
    create_entry_ledger_entry
)
from app.schemas import RaffleCreate, ProofReview, EntryLedgerCreate
from app.deps import get_current_user
from app.models import User

router = APIRouter()

# For now, we'll use a simple admin check - in production you'd want proper role management
def get_current_admin(current_user: User = Depends(get_current_user)):
    # Simple admin check - you can enhance this later
    if not current_user.email.endswith("@admin.com"):  # Simple admin check
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Raffle Management
@router.post("/raffles/", response_model=dict)
def create_new_raffle(
    raffle: RaffleCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new raffle"""
    return create_raffle(db=db, raffle=raffle)

@router.get("/raffles/", response_model=List[dict])
def list_all_raffles(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all raffles"""
    raffles = get_all_raffles(db, skip=skip, limit=limit)
    return [
        {
            "id": raffle.id,
            "title": raffle.title,
            "headline_prize": raffle.headline_prize,
            "month_key": raffle.month_key,
            "is_active": raffle.is_active,
            "created_at": raffle.created_at
        }
        for raffle in raffles
    ]

@router.put("/raffles/{raffle_id}/activate")
def activate_raffle(
    raffle_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Activate a raffle (deactivates all others)"""
    from app.models import Raffle
    
    # First deactivate all raffles
    db.query(Raffle).update({Raffle.is_active: False})
    
    # Then activate the specified raffle
    raffle = db.query(Raffle).filter(Raffle.id == raffle_id).first()
    if not raffle:
        raise HTTPException(status_code=404, detail="Raffle not found")
    
    raffle.is_active = True
    db.commit()
    
    return {"message": f"Raffle '{raffle.title}' activated"}

# Proof Management
@router.get("/proofs/pending", response_model=List[dict])
def list_pending_proofs(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all pending proof uploads"""
    proofs = get_pending_proofs(db, skip=skip, limit=limit)
    return [
        {
            "id": proof.id,
            "user_id": proof.user_id,
            "raffle_id": proof.raffle_id,
            "kind": proof.kind,
            "file_path": proof.file_path,
            "created_at": proof.created_at
        }
        for proof in proofs
    ]

@router.post("/proofs/{proof_id}/review")
def review_proof_upload(
    proof_id: int,
    review: ProofReview,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Review and approve/reject a proof upload"""
    result = review_proof(
        db=db,
        proof_id=proof_id,
        status=review.status,
        amount=review.amount
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Proof not found")
    
    if review.status == "approved":
        return {"message": "Proof approved and entries awarded"}
    else:
        return {"message": "Proof rejected"}

# Entry Management
@router.post("/entries/award")
def award_entries(
    user_id: int,
    raffle_id: int,
    amount: int,
    source: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Award entries to a user"""
    entry = EntryLedgerCreate(
        raffle_id=raffle_id,
        source=source,
        amount=amount
    )
    
    result = create_entry_ledger_entry(db=db, entry=entry, user_id=user_id)
    return {"message": f"Awarded {amount} entries to user {user_id}"}

# Dashboard
@router.get("/dashboard")
def admin_dashboard(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard overview"""
    pending_proofs = get_pending_proofs(db, limit=1000)
    all_raffles = get_all_raffles(db, limit=1000)
    
    return {
        "pending_proofs_count": len(pending_proofs),
        "total_raffles": len(all_raffles),
        "active_raffles": len([r for r in all_raffles if r.is_active]),
        "recent_proofs": [
            {
                "id": proof.id,
                "user_id": proof.user_id,
                "kind": proof.kind,
                "created_at": proof.created_at
            }
            for proof in pending_proofs[:5]  # Show last 5
        ]
    }
