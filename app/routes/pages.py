from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def index_page(request: Request):
    """Serve the main index page"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/about")
async def about_page(request: Request):
    """Serve the about page"""
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/contact")
async def contact_page(request: Request):
    """Serve the contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})

@router.get("/dashboard")
async def dashboard_page(request: Request):
    """Serve the dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/register")
async def register_page(request: Request):
    """Serve the registration page"""
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
async def login_page(request: Request):
    """Serve the login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/earn-entries")
async def earn_entries_page(request: Request):
    """Serve the earn entries page"""
    return templates.TemplateResponse("earn-entries.html", {"request": request})

@router.get("/admin")
async def admin_page(request: Request):
    """Serve the admin dashboard page"""
    return templates.TemplateResponse("admin.html", {"request": request})

@router.get("/welcome")
async def welcome_page(request: Request):
    """Serve the welcome/how-it-works page"""
    return templates.TemplateResponse("welcome.html", {"request": request})

@router.get("/pricing")
async def pricing_page(request: Request):
    """Serve the pricing page"""
    return templates.TemplateResponse("pricing.html", {"request": request})
