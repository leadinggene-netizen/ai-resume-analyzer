"""
Pricing and Subscription Page with Stripe and PayPal Integration
"""
import streamlit as st
import requests
import json
from stripe_integration import show_payment_button as show_stripe_button
from paypal_integration import show_paypal_button

st.set_page_config(
    page_title="Pricing - AI Resume Analyzer",
    page_icon="💳",
    layout="wide"
)

def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Create Stripe checkout session (you'll need to implement Stripe integration)"""
    # This is a placeholder - you'll implement actual Stripe integration
    pass

def main():
    st.title("💳 Choose Your Plan")
    st.markdown("Select the perfect plan for your career advancement needs!")
    
    # Pricing cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🆓 Free Plan
        **$0/month**
        
        ✅ 3 resume analyses per month  
        ✅ Basic PDF reports  
        ✅ Standard templates  
        ❌ No job optimization  
        ❌ No premium support  
        
        ---
        **Perfect for:** Occasional users
        """)
        
        if st.session_state.get('user_subscription') == 'free':
            st.success("✅ Current Plan")
        else:
            if st.button("Select Free Plan", key="free_plan"):
                st.session_state.user_subscription = 'free'
                st.session_state.usage_count = 0
                st.success("Switched to Free Plan!")
                st.rerun()
    
    with col2:
        st.markdown("""
        ### ⭐ Premium Plan
        **$9.99/month**
        
        ✅ Unlimited analyses  
        ✅ Job optimization  
        ✅ ATS compatibility check  
        ✅ Premium templates  
        ✅ Email support  
        ❌ No priority support  
        
        ---
        **Perfect for:** Active job seekers
        """)
        
        if st.session_state.get('user_subscription') == 'premium':
            st.success("✅ Current Plan")
        else:
            st.markdown("**Choose Payment Method:**")
            
            # Stripe payment button
            col_stripe, col_paypal = st.columns(2)
            with col_stripe:
                show_stripe_button("Premium", "9.99", st.secrets.get("STRIPE_PREMIUM_PRICE_ID"))
            with col_paypal:
                show_paypal_button("Premium", "9.99", st.secrets.get("PAYPAL_PREMIUM_PLAN_ID"))
            
            # Demo button for testing
            if st.button("🎮 Demo Premium (Testing)", key="demo_premium"):
                st.session_state.user_subscription = 'premium'
                st.success("🎉 Demo Premium Activated!")
                st.balloons()
                st.rerun()
    
    with col3:
        st.markdown("""
        ### 🌟 Pro Plan
        **$19.99/month**
        
        ✅ Everything in Premium  
        ✅ Cover letter generation  
        ✅ Interview prep questions  
        ✅ Priority support  
        ✅ Advanced analytics  
        ✅ Custom branding  
        
        ---
        **Perfect for:** Career professionals
        """)
        
        if st.session_state.get('user_subscription') == 'pro':
            st.success("✅ Current Plan")
        else:
            st.markdown("**Choose Payment Method:**")
            
            # Stripe payment button
            col_stripe_pro, col_paypal_pro = st.columns(2)
            with col_stripe_pro:
                show_stripe_button("Pro", "19.99", st.secrets.get("STRIPE_PRO_PRICE_ID"))
            with col_paypal_pro:
                show_paypal_button("Pro", "19.99", st.secrets.get("PAYPAL_PRO_PLAN_ID"))
            
            # Demo button for testing
            if st.button("🎮 Demo Pro (Testing)", key="demo_pro"):
                st.session_state.user_subscription = 'pro'
                st.success("🚀 Demo Pro Activated!")
                st.balloons()
                st.rerun()
    
    # Payment methods section
    st.markdown("---")
    st.markdown("### 💳 Payment Options")
    
    col_pay1, col_pay2, col_pay3 = st.columns(3)
    
    with col_pay1:
        st.markdown("""
        #### 🔄 Monthly Subscription
        - Automatic renewal
        - Cancel anytime
        - Full feature access
        """)
        
    with col_pay2:
        st.markdown("""
        #### 💰 Pay Per Use
        - $2.99 per analysis
        - No monthly commitment
        - Premium features included
        """)
        col_single_stripe, col_single_paypal = st.columns(2)
        with col_single_stripe:
            show_stripe_button("Single Analysis", "2.99", st.secrets.get("STRIPE_SINGLE_PRICE_ID"))
        with col_single_paypal:
            show_paypal_button("Single Analysis", "2.99")
            
    with col_pay3:
        st.markdown("""
        #### 🏢 Enterprise
        - Custom pricing
        - Volume discounts
        - Priority support
        """)
        if st.button("Contact Sales"):
            st.markdown("📧 Email: enterprise@your-domain.com")
    
    # FAQ Section
    st.markdown("---")
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("What's included in each plan?"):
        st.markdown("""
        - **Free**: Basic resume analysis with usage limits
        - **Premium**: Unlimited analyses + job optimization features
        - **Pro**: Everything + cover letters + interview prep + priority support
        """)
    
    with st.expander("Can I cancel anytime?"):
        st.markdown("Yes! You can cancel your subscription at any time. You'll continue to have access until the end of your billing period.")
    
    with st.expander("Do I need my own API key?"):
        st.markdown("""
        - **Free Plan**: Yes, you need your own OpenAI/SiliconFlow API key
        - **Premium/Pro**: We provide managed API access, no setup required!
        """)
    
    with st.expander("What payment methods do you accept?"):
        st.markdown("We accept all major credit cards, PayPal, and bank transfers for enterprise customers.")
    
    # Contact section
    st.markdown("---")
    st.markdown("### 📞 Need Help?")
    col_contact1, col_contact2 = st.columns(2)
    
    with col_contact1:
        st.markdown("**📧 Email Support**")
        st.markdown("support@your-domain.com")
        
    with col_contact2:
        st.markdown("**💬 Live Chat**")
        if st.button("Start Chat"):
            st.info("Chat feature coming soon!")

if __name__ == "__main__":
    main()