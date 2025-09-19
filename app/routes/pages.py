from fastapi import APIRouter, Request , Depends , status
from fastapi.templating import Jinja2Templates

from app.deps import get_current_user_optional
from fastapi.responses import RedirectResponse



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
async def register_page(request: Request , user=Depends(get_current_user_optional)):
    """Serve the registration page"""
    if user:  
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
async def login_page(request: Request, user=Depends(get_current_user_optional)):
    """Serve the login page or redirect if logged in"""
    if user:  
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    
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

@router.get("/forget-password")
async def pricing_page(request: Request):
    """Serve the forget password page"""
    return templates.TemplateResponse("forget.html", {"request": request})

@router.get("/sales-test209")
async def sales_page(request: Request):
    """Professional sales page for the platform"""
    return templates.TemplateResponse("sales-test209.html", {"request": request})

@router.get("/sales-test210")
async def customer_sales_page(request: Request):
    """Customer-facing sales page for licensing services"""
    return templates.TemplateResponse("sales-test210.html", {"request": request})

@router.get("/jjj")
async def giveaway_page(request: Request):
    """Giveaway landing page - Win a $15,000 raffle business"""
    return templates.TemplateResponse("jjj.html", {"request": request})

