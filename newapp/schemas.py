from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Raffle schemas
class RaffleBase(BaseModel):
    title: str
    month_key: str
    headline_prize: str

class RaffleCreate(RaffleBase):
    pass

class Raffle(RaffleBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Entry Ledger schemas
class EntryLedgerBase(BaseModel):
    raffle_id: int
    source: str  # 'base', 'vote', 'share', 'upload'
    amount: int

class EntryLedgerCreate(EntryLedgerBase):
    pass

class EntryLedger(EntryLedgerBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Proof Upload schemas
class ProofUploadBase(BaseModel):
    raffle_id: int
    kind: str  # 'share' | 'vote' | 'content'

class ProofUploadCreate(ProofUploadBase):
    pass

class ProofUpload(ProofUploadBase):
    id: int
    user_id: int
    file_path: str
    status: str  # 'pending' | 'approved' | 'rejected'
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Admin schemas
class ProofReview(BaseModel):
    status: str  # 'approved' | 'rejected'
    amount: Optional[int] = None  # Points to award if approved

# Dashboard schemas
class UserDashboard(BaseModel):
    user: User
    current_raffle: Optional[Raffle] = None
    total_entries: int = 0
    base_entries: int = 0
    vote_entries: int = 0
    share_entries: int = 0
    upload_entries: int = 0
    pending_proofs: List[ProofUpload] = []

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Shared fields
class VoteBase(BaseModel):
    year: int
    month: int
    prize_name: str

# For creating a vote (request body)
class VoteCreate(VoteBase):
    pass

# For returning a vote (response)
class VoteResponse(VoteBase):
    vote_id: int   # include primary key in response
    class Config:
        orm_mode = True  # allows ORM objects (SQLAlchemy) to be converted to Pydantic
