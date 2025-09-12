from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)  # replace with real auth later
    is_active = Column(Boolean, default=False)
    verification_token = Column(String(255), unique=True, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Raffle(Base):
    __tablename__ = "raffles"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    month_key = Column(String(7), nullable=False, index=True)  # e.g. "2025-09"
    headline_prize = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('month_key', name='uq_raffles_month_key'),)

class EntryLedger(Base):
    __tablename__ = "entry_ledger"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    raffle_id = Column(Integer, ForeignKey("raffles.id", ondelete="CASCADE"), index=True, nullable=False)
    source = Column(String(50), nullable=False)   # 'base', 'vote', 'share', 'upload'
    amount = Column(Integer, nullable=False)      # positive integers
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User")
    raffle = relationship("Raffle")

class ProofUpload(Base):
    __tablename__ = "proof_uploads"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    raffle_id = Column(Integer, ForeignKey("raffles.id", ondelete="CASCADE"), index=True, nullable=False)
    kind = Column(String(30), nullable=False)     # 'share' | 'vote' | 'content'
    file_path = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending | approved | rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
