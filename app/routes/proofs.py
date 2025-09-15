from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime

from app.db import get_db
from app.crud import create_proof_upload, get_user_proofs, get_active_raffle
from app.schemas import ProofUploadCreate, ProofUpload
from app.deps import get_current_user
from app.models import User

router = APIRouter()

UPLOAD_DIR = "static/social-proof"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ProofUpload)
async def create_proof_upload_endpoint(
    raffle_id: int = Form(...),
    kind: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read file in memory to check its length
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    # Validate raffle
    active_raffle = get_active_raffle(db)
    if not active_raffle or active_raffle.id != raffle_id:
        raise HTTPException(status_code=400, detail="Invalid or inactive raffle")

    # Save file
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Record in DB
    proof_data = ProofUploadCreate(raffle_id=raffle_id, kind=kind)
    return create_proof_upload(
        db=db,
        proof=proof_data,
        user_id=current_user.id,
        file_path=file_path
    )

@router.get("/", response_model=List[ProofUpload])
def read_user_proofs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all proof uploads for the current user"""
    proofs = get_user_proofs(db, user_id=current_user.id, skip=skip, limit=limit)
    return proofs

@router.get("/my-proofs", response_model=List[ProofUpload])
def get_my_proofs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all proof uploads for the current user (dashboard endpoint)"""
    proofs = get_user_proofs(db, user_id=current_user.id)
    return proofs

@router.get("/{proof_id}", response_model=ProofUpload)
def read_proof(
    proof_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific proof upload by ID"""
    proofs = get_user_proofs(db, user_id=current_user.id)
    proof = next((p for p in proofs if p.id == proof_id), None)
    if proof is None:
        raise HTTPException(status_code=404, detail="Proof not found")
    return proof

@router.get("/raffle/{raffle_id}", response_model=List[ProofUpload])
def read_user_proofs_for_raffle(
    raffle_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all proof uploads for a specific raffle"""
    proofs = get_user_proofs(db, user_id=current_user.id)
    raffle_proofs = [p for p in proofs if p.raffle_id == raffle_id]
    return raffle_proofs
