# Streamlit Multi-Page Configuration
# This tells Streamlit to use the multi-page structure

import streamlit as st

# Set global page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'user_subscription' not in st.session_state:
    st.session_state.user_subscription = 'free'

if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0

if 'user_email' not in st.session_state:
    st.session_state.user_email = 'demo@example.com'

# Navigation helper functions
def show_upgrade_prompt():
    """Show upgrade prompt for free users who hit limits"""
    st.error("🚫 Free plan limit reached!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Upgrade to Premium"):
            st.switch_page("pages/2_💳_Pricing.py")
    with col2:
        if st.button("👤 Manage Account"):
            st.switch_page("pages/3_👤_Account.py")

def show_subscription_status():
    """Show current subscription status in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Your Plan")
        
        subscription = st.session_state.get('user_subscription', 'free')
        usage = st.session_state.get('usage_count', 0)
        
        if subscription == 'free':
            remaining = max(0, 3 - usage)
            if remaining > 0:
                st.info(f"🆓 Free: {remaining} analyses left")
            else:
                st.error("🚫 Free limit reached")
                if st.button("🚀 Upgrade"):
                    st.switch_page("pages/2_💳_Pricing.py")
        elif subscription == 'premium':
            st.success("⭐ Premium Plan Active")
        elif subscription == 'pro':
            st.success("🌟 Pro Plan Active")
        
        # Quick navigation
        st.markdown("### 🧭 Navigation")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("Home.py")
        if st.button("💳 Pricing", use_container_width=True):
            st.switch_page("pages/2_💳_Pricing.py")
        if st.button("👤 Account", use_container_width=True):
            st.switch_page("pages/3_👤_Account.py")