"""
Stripe payment routes for LuckyClub WINS
Handles giveaway upgrades and license purchases
"""

import os
import stripe
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db import get_db
from app.utils.stripe_config import stripe_config
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Initialize Stripe with your secret key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # Add this to your .env file

@router.post("/create-checkout-session")
async def create_checkout_session(
    request: Request,
    tier: str,
    db: Session = Depends(get_db)
):
    """Create a Stripe checkout session for giveaway upgrades"""
    
    try:
        # Validate tier
        valid_tiers = ['silver', 'gold', 'white_label', 'api_license', 'hosted']
        if tier not in valid_tiers:
            raise HTTPException(status_code=400, detail=f"Invalid tier: {tier}")
        
        # Get price ID from config
        price_id = stripe_config.get_price_id_for_tier(tier)
        if not price_id:
            raise HTTPException(status_code=500, detail=f"Price ID not found for tier: {tier}")
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{request.base_url}payment-success?session_id={{CHECKOUT_SESSION_ID}}&tier={tier}",
            cancel_url=f"{request.base_url}upgrade-entries?cancelled=true",
            metadata={
                'tier': tier,
                'product_type': 'giveaway_upgrade' if tier in ['silver', 'gold'] else 'license',
                'user_ip': request.client.host
            }
        )
        
        return {"checkout_url": checkout_session.url}
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating checkout session: {str(e)}")

@router.get("/payment-success")
async def payment_success(
    session_id: str,
    tier: str,
    db: Session = Depends(get_db)
):
    """Handle successful payment and redirect to success page"""
    
    try:
        # Retrieve the checkout session
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            # TODO: Update user's giveaway entry in database
            # TODO: Send confirmation email
            # TODO: Add to appropriate tier
            
            # For now, redirect to success page with tier info
            return RedirectResponse(
                url=f"/payment-success-page?tier={tier}&session_id={session_id}",
                status_code=303
            )
        else:
            return RedirectResponse(
                url="/upgrade-entries?error=payment_failed",
                status_code=303
            )
            
    except stripe.error.StripeError as e:
        return RedirectResponse(
            url=f"/upgrade-entries?error=stripe_error&message={str(e)}",
            status_code=303
        )

@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks for payment confirmations"""
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')  # Add this to your .env
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # TODO: Update database with successful payment
        # TODO: Send confirmation email
        # TODO: Update user's giveaway entries
        
        print(f"Payment successful for session: {session['id']}")
        print(f"Tier: {session['metadata'].get('tier')}")
        
    return {"status": "success"}

# Example usage in your templates:
"""
<!-- Add this JavaScript to your upgrade-entries.html -->
<script>
async function upgradeToTier(tier) {
    try {
        const response = await fetch('/api/stripe/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ tier: tier })
        });
        
        const data = await response.json();
        
        if (data.checkout_url) {
            window.location.href = data.checkout_url;
        } else {
            alert('Error creating checkout session');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error processing upgrade');
    }
}
</script>
"""
