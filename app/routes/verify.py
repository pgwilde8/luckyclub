from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request
from app.db import get_db
from app.models import User

router = APIRouter(prefix="/api/verify", tags=["verify"])
templates = Jinja2Templates(directory="app/templates")  # path to your templates folder

@router.get("/{token}", response_class=HTMLResponse)
def verify_email(token: str, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()

    if not user:
        return templates.TemplateResponse(
            "verify.html",
            {"request": request, "success": False, "message": "Invalid or expired token"}
        )

    user.is_active = True
    user.verification_token = None
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse(
        "verify.html",
        {"request": request, "success": True, "message": "Email successfully verified"}
    )