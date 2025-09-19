from sqlalchemy.orm import Session
from app.models import User, Raffle, EntryLedger, ProofUpload,Vote
from app.schemas import UserCreate, RaffleCreate, EntryLedgerCreate, ProofUploadCreate
from passlib.context import CryptContext
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from newapp.utils.brevo_email import send_verification_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# Password utilities
def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# User operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    token = str(uuid4())
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        verification_token=token

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    send_verification_email(user.email,token)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Raffle operations
def create_raffle(db: Session, raffle: RaffleCreate):
    db_raffle = Raffle(**raffle.dict())
    db.add(db_raffle)
    db.commit()
    db.refresh(db_raffle)
    return db_raffle

def get_active_raffle(db: Session):
    return db.query(Raffle).filter(Raffle.is_active == True).first()

def get_raffle_by_month(db: Session, month_key: str):
    return db.query(Raffle).filter(Raffle.month_key == month_key).first()

def get_all_raffles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Raffle).offset(skip).limit(limit).all()

# Entry Ledger operations
def create_entry_ledger_entry(db: Session, entry: EntryLedgerCreate, user_id: int):
    db_entry = EntryLedger(**entry.dict(), user_id=user_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_user_entries_for_raffle(db: Session, user_id: int, raffle_id: int):
    return db.query(EntryLedger).filter(
        EntryLedger.user_id == user_id,
        EntryLedger.raffle_id == raffle_id
    ).all()

def get_user_total_entries_for_raffle(db: Session, user_id: int, raffle_id: int):
    entries = get_user_entries_for_raffle(db, user_id, raffle_id)
    return sum(entry.amount for entry in entries)

def get_user_entries_by_source(db: Session, user_id: int, raffle_id: int, source: str):
    return db.query(EntryLedger).filter(
        EntryLedger.user_id == user_id,
        EntryLedger.raffle_id == raffle_id,
        EntryLedger.source == source
    ).all()

def get_user_entries_summary(db: Session, user_id: int, raffle_id: int):
    """Get summary of user entries by source for a specific raffle"""
    entries = get_user_entries_for_raffle(db, user_id, raffle_id)
    
    summary = {
        'total': 0,
        'base': 0,
        'vote': 0,
        'share': 0,
        'upload': 0
    }
    
    for entry in entries:
        summary['total'] += entry.amount
        if entry.source == 'base':
            summary['base'] += entry.amount
        elif entry.source == 'vote':
            summary['vote'] += entry.amount
        elif entry.source == 'share':
            summary['share'] += entry.amount
        elif entry.source == 'upload':
            summary['upload'] += entry.amount
    
    return summary

# Proof Upload operations
def create_proof_upload(db: Session, proof: ProofUploadCreate, user_id: int, file_path: str):
    db_proof = ProofUpload(
        **proof.dict(),
        user_id=user_id,
        file_path=file_path
    )
    db.add(db_proof)
    db.commit()
    db.refresh(db_proof)
    return db_proof

def get_pending_proofs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProofUpload).filter(
        ProofUpload.status == "pending"
    ).offset(skip).limit(limit).all()

def get_user_proofs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ProofUpload).filter(ProofUpload.user_id == user_id).offset(skip).limit(limit).all()

def review_proof(db: Session, proof_id: int, status: str, amount: int = None):
    proof = db.query(ProofUpload).filter(ProofUpload.id == proof_id).first()
    if not proof:
        return None
    
    proof.status = status
    proof.reviewed_at = datetime.utcnow()
    
    # If approved and amount specified, create entry ledger entry
    if status == "approved" and amount and amount > 0:
        entry = EntryLedgerCreate(
            raffle_id=proof.raffle_id,
            source="upload",
            amount=amount
        )
        create_entry_ledger_entry(db, entry, proof.user_id)
    
    db.commit()
    db.refresh(proof)
    return proof


def save_vote(db: Session, user_id: int, year: int, month: int, prize_name: str):
    """
    Save a new vote in the votes table.
    Only one vote per user per year+month is allowed.
    """
 

    # create new vote
    new_vote = Vote(
        user_id=user_id,
        year=year,
        month=month,
        prize_name=prize_name
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote