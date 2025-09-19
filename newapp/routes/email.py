from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import APIRouter, Depends, HTTPException



router = APIRouter(
    prefix="/api/email",
    tags=["email"]
)

conf = ConnectionConfig(
    MAIL_USERNAME="villavizacamilo31@gmail.com",   # your Gmail
    MAIL_PASSWORD="mqjj ttcy kgym ublo",           # your App Password
    MAIL_FROM="luckyclubwins@gmail.com",           # sender email (can be same as username)
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

@router.get("/send-email")
async def send_test_email():
    message = MessageSchema(
        subject="Test Email",
        recipients=["villavizacamilo31@gmail.com"],  # 👈 put your email to receive test
        body="Hello! This is a test email from FastAPI 🚀",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "Email sent successfully!"}