"""
Account Management and Subscription Dashboard
"""
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="My Account - AI Resume Analyzer",
    page_icon="👤",
    layout="wide"
)

def main():
    st.title("👤 My Account")
    
    # Initialize user data if not exists
    if 'user_email' not in st.session_state:
        st.session_state.user_email = "demo@example.com"
    if 'user_subscription' not in st.session_state:
        st.session_state.user_subscription = 'free'
    if 'subscription_start' not in st.session_state:
        st.session_state.subscription_start = datetime.now()
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    
    # Account overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Account Overview")
        
        # User info
        st.markdown(f"**Email:** {st.session_state.user_email}")
        st.markdown(f"**Plan:** {st.session_state.user_subscription.title()}")
        st.markdown(f"**Member since:** {st.session_state.subscription_start.strftime('%B %Y')}")
        
        # Usage statistics
        st.markdown("---")
        st.markdown("### 📈 Usage Statistics")
        
        if st.session_state.user_subscription == 'free':
            st.metric("Analyses This Month", st.session_state.usage_count, "of 3 allowed")
            remaining = max(0, 3 - st.session_state.usage_count)
            if remaining == 0:
                st.error("🚫 Monthly limit reached!")
                if st.button("Upgrade to Premium"):
                    st.switch_page("pages/2_💳_Pricing.py")
        else:
            st.metric("Analyses This Month", st.session_state.usage_count, "unlimited")
            st.success("✅ Unlimited access active")
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("🏠 Analyze Resume", use_container_width=True):
            st.switch_page("Home.py")
            
        if st.button("💳 Change Plan", use_container_width=True):
            st.switch_page("pages/2_💳_Pricing.py")
            
        if st.button("📧 Contact Support", use_container_width=True):
            st.markdown("**Email:** support@your-domain.com")
            
        if st.button("🔄 Reset Usage (Demo)", use_container_width=True):
            st.session_state.usage_count = 0
            st.success("Usage reset!")
            st.rerun()
    
    # Subscription management
    st.markdown("---")
    st.markdown("### 💳 Subscription Management")
    
    if st.session_state.user_subscription == 'free':
        st.info("You're on the free plan. Upgrade to unlock premium features!")
        col_upgrade1, col_upgrade2 = st.columns(2)
        with col_upgrade1:
            if st.button("Upgrade to Premium ($9.99/mo)"):
                st.session_state.user_subscription = 'premium'
                st.success("Upgraded to Premium!")
                st.rerun()
        with col_upgrade2:
            if st.button("Upgrade to Pro ($19.99/mo)"):
                st.session_state.user_subscription = 'pro'
                st.success("Upgraded to Pro!")
                st.rerun()
    else:
        # Active subscription info
        next_billing = st.session_state.subscription_start + timedelta(days=30)
        st.success(f"✅ {st.session_state.user_subscription.title()} plan active")
        st.markdown(f"**Next billing date:** {next_billing.strftime('%B %d, %Y')}")
        
        col_manage1, col_manage2 = st.columns(2)
        with col_manage1:
            if st.button("📄 Download Invoice"):
                st.info("Invoice download feature coming soon!")
        with col_manage2:
            if st.button("❌ Cancel Subscription"):
                with st.expander("Are you sure you want to cancel?"):
                    st.warning("You'll lose access to premium features at the end of your billing period.")
                    if st.button("Yes, Cancel Subscription"):
                        st.session_state.user_subscription = 'free'
                        st.error("Subscription cancelled. You can reactivate anytime!")
                        st.rerun()
    
    # Usage history
    st.markdown("---")
    st.markdown("### 📊 Usage History")
    
    # Mock usage data
    import pandas as pd
    import numpy as np
    
    # Generate sample usage data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    usage_data = pd.DataFrame({
        'Date': dates,
        'Analyses': np.random.poisson(0.3, len(dates))  # Random usage pattern
    })
    
    # Aggregate by month
    monthly_usage = usage_data.groupby(usage_data['Date'].dt.to_period('M'))['Analyses'].sum()
    
    st.bar_chart(monthly_usage)
    
    # Recent activity
    st.markdown("### 📋 Recent Activity")
    
    activity_data = [
        {"Date": "2024-09-30", "Activity": "Resume analyzed", "Plan": "Premium"},
        {"Date": "2024-09-29", "Activity": "Job optimization used", "Plan": "Premium"},
        {"Date": "2024-09-28", "Activity": "PDF report generated", "Plan": "Premium"},
        {"Date": "2024-09-27", "Activity": "Upgraded to Premium", "Plan": "Premium"},
        {"Date": "2024-09-26", "Activity": "Account created", "Plan": "Free"}
    ]
    
    for activity in activity_data[:5]:  # Show last 5 activities
        col_date, col_activity, col_plan = st.columns([1, 2, 1])
        with col_date:
            st.text(activity["Date"])
        with col_activity:
            st.text(activity["Activity"])
        with col_plan:
            if activity["Plan"] == "Premium":
                st.success("Premium")
            else:
                st.info("Free")
    
    # Settings
    st.markdown("---")
    st.markdown("### ⚙️ Account Settings")
    
    with st.expander("Update Profile"):
        new_email = st.text_input("Email Address", value=st.session_state.user_email)
        if st.button("Update Email"):
            st.session_state.user_email = new_email
            st.success("Email updated!")
    
    with st.expander("Notification Preferences"):
        st.checkbox("Email notifications for usage limits", value=True)
        st.checkbox("Monthly usage reports", value=True)
        st.checkbox("Product updates and news", value=False)
        if st.button("Save Preferences"):
            st.success("Preferences saved!")
    
    with st.expander("Data & Privacy"):
        st.markdown("**Data Retention:** We keep your data for 12 months after account deletion.")
        st.markdown("**Privacy Policy:** [View our privacy policy](https://your-domain.com/privacy)")
        if st.button("Download My Data"):
            st.info("Data export feature coming soon!")
        if st.button("Delete Account", type="secondary"):
            st.error("Account deletion is permanent and cannot be undone!")

if __name__ == "__main__":
    main()