from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.routes import auth, entries, proofs, health, admin, pages, raffles,verify,email,vote
from app.db import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create sample data for testing
def create_sample_data():
    try:
        from app.db import get_db
        from app.crud import create_raffle, create_entry_ledger_entry, create_proof_upload
        from app.schemas import RaffleCreate, EntryLedgerCreate, ProofUploadCreate
        from app.models import User, Raffle
        
        db = next(get_db())
        
        # Check if we already have data
        existing_raffle = db.query(Raffle).first()
        if existing_raffle:
            return  # Already have data
        
        # Create a sample raffle
        raffle_data = RaffleCreate(
            title="January 2024 Laptop Raffle",
            month_key="2024-01",
            headline_prize="Dell XPS 13 Laptop + $500 Cash"
        )
        raffle = create_raffle(db, raffle_data)
        
        # Get the first user (if any exist)
        user = db.query(User).first()
        if user:
            # Create sample entries
            entry_data = EntryLedgerCreate(
                raffle_id=raffle.id,
                source="base",
                amount=15
            )
            create_entry_ledger_entry(db, entry_data, user.id)
            
            # Create sample proof
            proof_data = ProofUploadCreate(
                raffle_id=raffle.id,
                kind="screenshot"
            )
            create_proof_upload(db, proof_data, user.id, "sample_proof.jpg")
    except Exception as e:
        print(f"Sample data creation failed: {e}")
        # Continue without sample data

# Create sample data
create_sample_data()

app = FastAPI(title="LuckyClub API", version="1.0.0")

# Mount static files

app.mount("/social-proof", StaticFiles(directory="static/social-proof"), name="social-proof")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(pages.router, tags=["pages"])  # Static pages first
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(entries.router, prefix="/api/entries", tags=["entries"])
app.include_router(proofs.router, prefix="/api/proofs", tags=["proofs"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(vote.router, prefix="/api/vote", tags=["vote"])
app.include_router(raffles.router)
app.include_router(verify.router)
app.include_router(email.router)
# @app.get("/")
# async def root():
#     return {"message": "Welcome to LuckyClub API", "port": 9177}

# @app.get("/api/raffles/current")
# async def get_current_raffle():
#     """Get the currently active raffle"""
#     from app.crud import get_active_raffle
#     from app.db import get_db
    
#     db = next(get_db())
#     raffle = get_active_raffle(db)
#     if raffle:
#         return {
#             "id": raffle.id,
#             "title": raffle.title,
#             "headline_prize": raffle.headline_prize,
#             "month_key": raffle.month_key
#         }
#     return {"message": "No active raffle found"}

@app.get("/api/dashboard")
async def get_user_dashboard():
    """Get user dashboard data"""
    from app.crud import get_active_raffle, get_user_total_entries_for_raffle, get_user_proofs
    from app.db import get_db
    from app.deps import get_current_user
    
    # For now, return sample data
    # Later this will use get_current_user to get real user data
    return {
        "current_raffle": {
            "title": "January 2024 Laptop Raffle",
            "headline_prize": "Dell XPS 13 Laptop + $500 Cash",
            "month_key": "2024-01"
        },
        "user_stats": {
            "total_entries": 18,
            "base_entries": 15,
            "vote_entries": 0,
            "share_entries": 0,
            "upload_entries": 3
        },
        "pending_proofs": 2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9177)
