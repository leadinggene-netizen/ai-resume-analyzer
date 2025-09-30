"""
Utility functions for the AI Resume Analyzer
"""
import streamlit as st
from openai import OpenAI
import re
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from PyPDF2 import PdfReader
from docx import Document

API_BASE_URL = "https://api.siliconflow.cn/v1"

def check_subscription_limits():
    """Check if user can perform analysis based on their subscription"""
    subscription = st.session_state.get('user_subscription', 'free')
    usage_count = st.session_state.get('usage_count', 0)
    
    if subscription == 'free':
        if usage_count >= 3:
            return False, "Free plan limit reached (3 analyses per month)"
    
    return True, "Access granted"

def increment_usage():
    """Increment usage counter for free users"""
    if st.session_state.get('user_subscription', 'free') == 'free':
        st.session_state.usage_count = st.session_state.get('usage_count', 0) + 1

def get_user_features():
    """Get available features based on subscription level"""
    subscription = st.session_state.get('user_subscription', 'free')
    
    features = {
        'free': {
            'max_analyses': 3,
            'job_optimization': False,
            'premium_templates': False,
            'priority_support': False,
            'cover_letter': False
        },
        'premium': {
            'max_analyses': float('inf'),
            'job_optimization': True,
            'premium_templates': True,
            'priority_support': False,
            'cover_letter': False
        },
        'pro': {
            'max_analyses': float('inf'),
            'job_optimization': True,
            'premium_templates': True,
            'priority_support': True,
            'cover_letter': True
        }
    }
    
    return features.get(subscription, features['free'])

# Your existing functions from resume_analyzer.py can be moved here
def clean_text_for_pdf(text):
    """Clean text content to make it safe for PDF generation"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
    text = re.sub(r'`([^`]+)`', r'\1', text)        # Code
    text = re.sub(r'#+\s*', '', text)               # Headers
    text = re.sub(r'^-\s*', '• ', text, flags=re.MULTILINE)  # Bullet points
    
    # Remove excessive whitespace
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s.,!?;:()\[\]{}"\'-•]', '', text)
    
    return text.strip()

def analyze_resume_with_ai(resume_text, target_position, api_key):
    """Analyze resume using AI"""
    if not api_key or not api_key.strip():
        return "Enter your API key"
    
    client = OpenAI(api_key=api_key, base_url=API_BASE_URL)
    
    prompt = f"""
    As an expert HR professional and career advisor, please analyze the following resume for a {target_position} position.
    
    Resume Content:
    {resume_text}
    
    Please provide a comprehensive analysis including:
    1. Overall Assessment (strengths and weaknesses)
    2. Skills Analysis (relevant skills for the target position)
    3. Experience Evaluation (how well experience matches the role)
    4. Specific Recommendations for improvement
    5. Overall Score (1-10) with justification
    
    Format your response clearly with headers and bullet points.
    """
    
    try:
        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[
                {"role": "system", "content": "You are an expert HR professional and career advisor specializing in resume analysis."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error during analysis: {str(e)}"

# Add more utility functions as needed...