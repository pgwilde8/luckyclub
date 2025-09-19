import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = "villavizacamilo31@gmail.com"
SENDER_NAME = "LuckyClub WINS"

# Configure API client
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_verification_email(to_email: str, token: str):
    verification_link = f"http://localhost:9177/api/verify/{token}"
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"name": SENDER_NAME, "email": SENDER_EMAIL},
        subject="Verify Your LuckyClub Account",
        html_content=f"<p>Click <a href='{verification_link}'>here</a> to verify your email.</p>"
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        return response
    except ApiException as e:
        raise HTTPException(status_code=500, detail=f"Email failed: {e}")