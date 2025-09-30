"""
Main application page - Resume Analysis
"""
import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from docx import Document
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import re

# Import your existing functions (we'll move them to a utils file)
# from utils import analyze_resume_with_ai, generate_pdf_report, etc.

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Check user authentication/subscription status
    if 'user_subscription' not in st.session_state:
        st.session_state.user_subscription = 'free'  # free, premium, pro
    
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    
    # Display subscription status in sidebar
    with st.sidebar:
        st.markdown("### 📊 Your Plan")
        if st.session_state.user_subscription == 'free':
            remaining = max(0, 3 - st.session_state.usage_count)
            st.info(f"🆓 Free Plan: {remaining} analyses left")
            if remaining == 0:
                st.error("Upgrade to continue!")
                if st.button("🚀 Upgrade Now"):
                    st.switch_page("pages/2_💳_Pricing.py")
        elif st.session_state.user_subscription == 'premium':
            st.success("⭐ Premium Plan - Unlimited analyses")
        elif st.session_state.user_subscription == 'pro':
            st.success("🌟 Pro Plan - All features included")
            
        st.markdown("---")
        
    st.title("📄 AI Resume Analyzer")
    st.markdown("Get AI-powered insights to improve your resume!")
    
    # Your existing resume analysis functionality here
    # (We'll keep the core functionality in this main page)
    
    # API Key input
    api_key = st.text_input("Enter your API Key", type="password")
    
    if not api_key:
        st.warning("Please enter your API key to continue")
        st.markdown("### 🔗 Get Your API Key:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("[SiliconFlow](https://siliconflow.cn)")
        with col2:
            st.markdown("[OpenAI](https://platform.openai.com)")
        with col3:
            if st.button("🛍️ Or Buy Managed Service"):
                st.switch_page("pages/2_💳_Pricing.py")
        return
    
    # Resume upload and analysis (existing functionality)
    uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx', 'txt'])
    
    if uploaded_file and st.button("Analyze Resume"):
        # Check usage limits
        if st.session_state.user_subscription == 'free' and st.session_state.usage_count >= 3:
            st.error("Free limit reached! Please upgrade to continue.")
            if st.button("Upgrade Now", type="primary"):
                st.switch_page("pages/2_💳_Pricing.py")
            return
            
        # Increment usage for free users
        if st.session_state.user_subscription == 'free':
            st.session_state.usage_count += 1
            
        # Perform analysis (your existing code)
        st.success("Analysis complete!")

if __name__ == "__main__":
    main()