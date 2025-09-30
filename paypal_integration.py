"""
PayPal Integration for AI Resume Analyzer
"""
import streamlit as st
import requests
import base64
import json
from datetime import datetime

# PayPal Configuration
PAYPAL_CLIENT_ID = st.secrets.get("PAYPAL_CLIENT_ID", "your_paypal_client_id")
PAYPAL_CLIENT_SECRET = st.secrets.get("PAYPAL_CLIENT_SECRET", "your_paypal_client_secret")
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"  # Change to https://api-m.paypal.com for live
PAYPAL_MODE = st.secrets.get("PAYPAL_MODE", "sandbox")  # sandbox or live

if PAYPAL_MODE == "live":
    PAYPAL_BASE_URL = "https://api-m.paypal.com"

def get_paypal_access_token():
    """Get PayPal access token for API calls"""
    try:
        auth_string = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            'Authorization': f'Basic {auth_b64}',
            'Accept': 'application/json',
            'Accept-Language': 'en_US',
        }
        
        data = 'grant_type=client_credentials'
        
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            headers=headers,
            data=data
        )
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            st.error(f"PayPal auth error: {response.status_code}")
            return None
            
    except Exception as e:
        st.error(f"PayPal authentication failed: {str(e)}")
        return None

def create_paypal_subscription(plan_id, return_url, cancel_url):
    """Create PayPal subscription"""
    access_token = get_paypal_access_token()
    if not access_token:
        return None
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'PayPal-Request-Id': f'subscription-{datetime.now().timestamp()}',
        'Prefer': 'return=representation'
    }
    
    subscription_data = {
        "plan_id": plan_id,
        "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "subscriber": {
            "email_address": st.session_state.get('user_email', 'user@example.com')
        },
        "application_context": {
            "brand_name": "AI Resume Analyzer",
            "locale": "en-US",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "SUBSCRIBE_NOW",
            "payment_method": {
                "payer_selected": "PAYPAL",
                "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
            },
            "return_url": return_url,
            "cancel_url": cancel_url
        }
    }
    
    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/billing/subscriptions",
            headers=headers,
            json=subscription_data
        )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"PayPal subscription error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"PayPal subscription creation failed: {str(e)}")
        return None

def create_paypal_order(amount, currency="USD", description="AI Resume Analysis"):
    """Create PayPal order for one-time payments"""
    access_token = get_paypal_access_token()
    if not access_token:
        return None
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'PayPal-Request-Id': f'order-{datetime.now().timestamp()}'
    }
    
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": currency,
                "value": str(amount)
            },
            "description": description
        }],
        "application_context": {
            "brand_name": "AI Resume Analyzer",
            "landing_page": "NO_PREFERENCE",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "PAY_NOW"
        }
    }
    
    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            headers=headers,
            json=order_data
        )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"PayPal order error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        st.error(f"PayPal order creation failed: {str(e)}")
        return None

# PayPal Plan IDs (create these in PayPal dashboard)
PAYPAL_PLAN_IDS = {
    'premium_monthly': st.secrets.get("PAYPAL_PREMIUM_PLAN_ID", "P-premium-plan-id"),
    'pro_monthly': st.secrets.get("PAYPAL_PRO_PLAN_ID", "P-pro-plan-id")
}

def show_paypal_button(plan_type, amount, plan_id=None):
    """Show PayPal payment button"""
    if plan_id:  # Subscription
        if st.button(f"💙 Subscribe with PayPal - {plan_type} ${amount}/mo", key=f"paypal_sub_{plan_type}"):
            return_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}/pages/3_👤_Account.py?paypal_success=true"
            cancel_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}/pages/2_💳_Pricing.py?paypal_canceled=true"
            
            subscription = create_paypal_subscription(plan_id, return_url, cancel_url)
            if subscription:
                # Get approval URL
                approval_url = next((link['href'] for link in subscription.get('links', []) if link['rel'] == 'approve'), None)
                if approval_url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={approval_url}">', unsafe_allow_html=True)
                    st.info("Redirecting to PayPal...")
    else:  # One-time payment
        if st.button(f"💙 Pay ${amount} with PayPal", key=f"paypal_pay_{amount}"):
            order = create_paypal_order(amount, description=f"{plan_type} Analysis")
            if order:
                # Get approval URL
                approval_url = next((link['href'] for link in order.get('links', []) if link['rel'] == 'approve'), None)
                if approval_url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={approval_url}">', unsafe_allow_html=True)
                    st.info("Redirecting to PayPal...")

# Webhook handling for PayPal
def handle_paypal_webhook(headers, body):
    """Handle PayPal webhook events"""
    try:
        # Verify webhook signature (implement PayPal webhook verification)
        event_data = json.loads(body)
        event_type = event_data.get('event_type')
        
        if event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
            handle_paypal_subscription_activated(event_data)
        elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
            handle_paypal_subscription_cancelled(event_data)
        elif event_type == 'PAYMENT.CAPTURE.COMPLETED':
            handle_paypal_payment_completed(event_data)
            
        return True
    except Exception as e:
        st.error(f"PayPal webhook error: {str(e)}")
        return False

def handle_paypal_subscription_activated(event_data):
    """Handle PayPal subscription activation"""
    subscription_id = event_data['resource']['id']
    # Update user subscription status
    # In production, you'd update your database here

def handle_paypal_subscription_cancelled(event_data):
    """Handle PayPal subscription cancellation"""
    subscription_id = event_data['resource']['id']
    # Update user subscription status to free

def handle_paypal_payment_completed(event_data):
    """Handle PayPal one-time payment completion"""
    payment_id = event_data['resource']['id']
    amount = event_data['resource']['amount']['value']
    # Grant single analysis access