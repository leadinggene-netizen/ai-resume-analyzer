"""
Stripe Payment Integration for AI Resume Analyzer
"""
import streamlit as st
import stripe
import os
from datetime import datetime, timedelta

# Configure Stripe with your live credentials
try:
    stripe.api_key = st.secrets.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        # Fallback for local development
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
        st.warning("⚠️ Using test Stripe key. Add STRIPE_SECRET_KEY to Streamlit secrets for production.")
except:
    st.error("❌ Stripe configuration error. Please check your API keys.")

# Stripe Price IDs - You'll create these in your Stripe dashboard
PRICE_IDS = {
    'premium_monthly': st.secrets.get("STRIPE_PREMIUM_PRICE_ID", "price_premium_monthly"),
    'pro_monthly': st.secrets.get("STRIPE_PRO_PRICE_ID", "price_pro_monthly"),
    'single_analysis': st.secrets.get("STRIPE_SINGLE_PRICE_ID", "price_single_analysis")
}

def create_checkout_session(price_id, success_url, cancel_url, customer_email=None):
    """Create a Stripe checkout session"""
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription' if 'monthly' in price_id else 'payment',
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=customer_email,
            metadata={
                'user_id': st.session_state.get('user_id', 'anonymous'),
                'plan_type': 'premium' if 'premium' in price_id else 'pro'
            }
        )
        return checkout_session
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None

def create_customer_portal_session(customer_id, return_url):
    """Create a Stripe customer portal session for subscription management"""
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return portal_session
    except Exception as e:
        st.error(f"Error creating portal session: {str(e)}")
        return None

def handle_webhook(payload, sig_header):
    """Handle Stripe webhooks for subscription updates"""
    endpoint_secret = st.secrets.get("STRIPE_WEBHOOK_SECRET")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return False
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return False
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Update user subscription in your database
        handle_successful_payment(session)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        # Handle subscription cancellation
        handle_subscription_cancelled(subscription)
    
    return True

def handle_successful_payment(session):
    """Handle successful payment completion"""
    # Update user subscription status
    user_id = session['metadata']['user_id']
    plan_type = session['metadata']['plan_type']
    
    # In a real app, you'd update your database here
    # For demo purposes, we'll update session state
    if 'user_id' in st.session_state and st.session_state['user_id'] == user_id:
        st.session_state.user_subscription = plan_type
        st.session_state.subscription_start = datetime.now()

def handle_subscription_cancelled(subscription):
    """Handle subscription cancellation"""
    # Update user subscription status to free
    customer_id = subscription['customer']
    
    # In a real app, you'd find the user by customer_id and update their status
    # For demo purposes:
    if 'stripe_customer_id' in st.session_state and st.session_state['stripe_customer_id'] == customer_id:
        st.session_state.user_subscription = 'free'

# Streamlit components for payment UI
def show_payment_button(plan_type, price, price_id):
    """Show payment button with Stripe integration"""
    if st.button(f"Subscribe to {plan_type} - ${price}/month", type="primary"):
        # Create checkout session
        success_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}/pages/3_👤_Account.py?success=true"
        cancel_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}/pages/2_💳_Pricing.py?canceled=true"
        
        checkout_session = create_checkout_session(
            price_id=price_id,
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=st.session_state.get('user_email')
        )
        
        if checkout_session:
            # Redirect to Stripe checkout
            st.markdown(f'<meta http-equiv="refresh" content="0; url={checkout_session.url}">', unsafe_allow_html=True)
            st.info("Redirecting to secure checkout...")

def show_manage_subscription_button():
    """Show button to manage existing subscription"""
    if st.button("Manage Subscription", type="secondary"):
        customer_id = st.session_state.get('stripe_customer_id')
        if customer_id:
            return_url = f"{st.secrets.get('APP_URL', 'http://localhost:8501')}/pages/3_👤_Account.py"
            portal_session = create_customer_portal_session(customer_id, return_url)
            
            if portal_session:
                st.markdown(f'<meta http-equiv="refresh" content="0; url={portal_session.url}">', unsafe_allow_html=True)
                st.info("Redirecting to subscription management...")
        else:
            st.error("No active subscription found.")

# Example usage in your pricing page:
def enhanced_pricing_page():
    """Enhanced pricing page with real Stripe integration"""
    st.title("💳 Choose Your Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col2:  # Premium plan
        st.markdown("### ⭐ Premium Plan")
        st.markdown("**$9.99/month**")
        st.markdown("✅ Unlimited analyses")
        st.markdown("✅ Job optimization")
        st.markdown("✅ Premium support")
        
        # Use real Stripe integration
        show_payment_button("Premium", "9.99", PRICE_IDS['premium_monthly'])
    
    with col3:  # Pro plan
        st.markdown("### 🌟 Pro Plan")
        st.markdown("**$19.99/month**")
        st.markdown("✅ Everything in Premium")
        st.markdown("✅ Cover letter generation")
        st.markdown("✅ Priority support")
        
        show_payment_button("Pro", "19.99", PRICE_IDS['pro_monthly'])

# Security considerations:
def validate_user_session():
    """Validate user session and subscription status"""
    # In production, verify with your database
    # Check if subscription is still active
    # Validate payment status with Stripe
    pass