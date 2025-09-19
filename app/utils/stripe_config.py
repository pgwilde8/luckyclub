"""
Stripe configuration utility for LuckyClub WINS
Loads Stripe product and price IDs from environment variables
"""

import os
from typing import Dict, Optional

class StripeConfig:
    """Centralized Stripe configuration from environment variables"""
    
    def __init__(self):
        # Load all Stripe IDs from environment
        self.WHITE_LABEL_PRODUCT_ID = os.getenv('STRIPE_WHITE_LABEL_PRODUCT_ID')
        self.WHITE_LABEL_PRICE_ID = os.getenv('STRIPE_WHITE_LABEL_PRICE_ID')
        
        self.API_LICENSE_PRODUCT_ID = os.getenv('STRIPE_API_LICENSE_PRODUCT_ID')
        self.API_LICENSE_PRICE_ID = os.getenv('STRIPE_API_LICENSE_PRICE_ID')
        
        self.HOSTED_PRODUCT_ID = os.getenv('STRIPE_HOSTED_PRODUCT_ID')
        self.HOSTED_PRICE_ID = os.getenv('STRIPE_HOSTED_PRICE_ID')
        
        self.SILVER_UPGRADE_PRODUCT_ID = os.getenv('STRIPE_SILVER_UPGRADE_PRODUCT_ID')
        self.SILVER_UPGRADE_PRICE_ID = os.getenv('STRIPE_SILVER_UPGRADE_PRICE_ID')
        
        self.GOLD_UPGRADE_PRODUCT_ID = os.getenv('STRIPE_GOLD_UPGRADE_PRODUCT_ID')
        self.GOLD_UPGRADE_PRICE_ID = os.getenv('STRIPE_GOLD_UPGRADE_PRICE_ID')
    
    def get_license_prices(self) -> Dict[str, Dict[str, str]]:
        """Get all license pricing information"""
        return {
            'white_label': {
                'product_id': self.WHITE_LABEL_PRODUCT_ID,
                'price_id': self.WHITE_LABEL_PRICE_ID,
                'name': 'White-Label License',
                'description': 'Full white-label raffle platform'
            },
            'api_license': {
                'product_id': self.API_LICENSE_PRODUCT_ID,
                'price_id': self.API_LICENSE_PRICE_ID,
                'name': 'API License',
                'description': 'API access to raffle platform'
            },
            'hosted': {
                'product_id': self.HOSTED_PRODUCT_ID,
                'price_id': self.HOSTED_PRICE_ID,
                'name': 'Professionally Hosted',
                'description': 'Fully managed hosting solution'
            }
        }
    
    def get_upgrade_prices(self) -> Dict[str, Dict[str, str]]:
        """Get giveaway upgrade pricing information"""
        return {
            'silver': {
                'product_id': self.SILVER_UPGRADE_PRODUCT_ID,
                'price_id': self.SILVER_UPGRADE_PRICE_ID,
                'name': 'Upgrade to Silver',
                'description': '10 entries + $500 discount + consultation'
            },
            'gold': {
                'product_id': self.GOLD_UPGRADE_PRODUCT_ID,
                'price_id': self.GOLD_UPGRADE_PRICE_ID,
                'name': 'Upgrade to Gold',
                'description': '25 entries + $1,000 discount + VIP access'
            }
        }
    
    def get_price_id_for_tier(self, tier: str) -> Optional[str]:
        """Get Stripe price ID for a specific tier"""
        tier_mapping = {
            'white_label': self.WHITE_LABEL_PRICE_ID,
            'api_license': self.API_LICENSE_PRICE_ID,
            'hosted': self.HOSTED_PRICE_ID,
            'silver': self.SILVER_UPGRADE_PRICE_ID,
            'gold': self.GOLD_UPGRADE_PRICE_ID
        }
        return tier_mapping.get(tier.lower())
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate that all required Stripe IDs are loaded"""
        config_status = {
            'white_label': bool(self.WHITE_LABEL_PRODUCT_ID and self.WHITE_LABEL_PRICE_ID),
            'api_license': bool(self.API_LICENSE_PRODUCT_ID and self.API_LICENSE_PRICE_ID),
            'hosted': bool(self.HOSTED_PRODUCT_ID and self.HOSTED_PRICE_ID),
            'silver_upgrade': bool(self.SILVER_UPGRADE_PRODUCT_ID and self.SILVER_UPGRADE_PRICE_ID),
            'gold_upgrade': bool(self.GOLD_UPGRADE_PRODUCT_ID and self.GOLD_UPGRADE_PRICE_ID)
        }
        return config_status

# Create singleton instance
stripe_config = StripeConfig()

# Example usage functions
def create_checkout_session_data(tier: str, success_url: str, cancel_url: str) -> Dict:
    """Create Stripe checkout session data for a specific tier"""
    price_id = stripe_config.get_price_id_for_tier(tier)
    
    if not price_id:
        raise ValueError(f"Invalid tier: {tier}")
    
    return {
        'line_items': [{
            'price': price_id,
            'quantity': 1,
        }],
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
        'metadata': {
            'tier': tier,
            'product_type': 'giveaway_upgrade' if tier in ['silver', 'gold'] else 'license'
        }
    }

def get_all_products_for_frontend() -> Dict:
    """Get all product data formatted for frontend use"""
    return {
        'licenses': stripe_config.get_license_prices(),
        'upgrades': stripe_config.get_upgrade_prices()
    }

if __name__ == "__main__":
    # Test the configuration
    print("Stripe Configuration Status:")
    print("-" * 40)
    
    status = stripe_config.validate_config()
    for product, is_configured in status.items():
        status_icon = "✅" if is_configured else "❌"
        print(f"{status_icon} {product.replace('_', ' ').title()}: {is_configured}")
    
    print("\nAvailable Products:")
    print("-" * 40)
    
    # Show licenses
    licenses = stripe_config.get_license_prices()
    for key, data in licenses.items():
        print(f"📦 {data['name']}: {data['price_id']}")
    
    # Show upgrades
    upgrades = stripe_config.get_upgrade_prices()
    for key, data in upgrades.items():
        print(f"⬆️ {data['name']}: {data['price_id']}")
