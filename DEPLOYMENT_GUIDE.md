# Multi-Page Payment System Deployment Guide

## 🚀 Quick Deployment Checklist

### 1. Stripe Setup (You have this ✅)
- [x] Stripe account active
- [ ] Create products in Stripe Dashboard:
  - Premium Monthly: $9.99/month (recurring)
  - Pro Monthly: $19.99/month (recurring)  
  - Single Analysis: $2.99 (one-time)
- [ ] Get Price IDs from Stripe Dashboard
- [ ] Set up webhook endpoint (we'll provide URL after deployment)

### 2. PayPal Setup (You have this ✅)
- [x] PayPal account active
- [ ] Create subscription plans in PayPal Dashboard:
  - Premium Monthly: $9.99/month
  - Pro Monthly: $19.99/month
- [ ] Get Plan IDs from PayPal Dashboard
- [ ] Configure webhook endpoint

### 3. Streamlit Cloud Deployment

#### A. Update Repository Structure
Your app will now use `Home.py` as the main file instead of `resume_analyzer.py`.

```
resumeAnalyzer/
├── Home.py                 # 👈 NEW MAIN FILE
├── pages/
│   ├── 2_💳_Pricing.py    # Payment & subscription page
│   └── 3_👤_Account.py    # Account management
├── stripe_integration.py  # Stripe payment logic
├── paypal_integration.py  # PayPal payment logic
├── utils.py               # Shared functions
└── requirements.txt       # Updated with payment libraries
```

#### B. Update Streamlit Cloud Settings
1. Go to your Streamlit Cloud app settings
2. Change **Main file path** from `resume_analyzer.py` to `Home.py`
3. Add all secrets from `secrets_template.toml` to the Secrets section

#### C. Required Secrets Configuration
```toml
# API Keys
OPENAI_API_KEY = "your_actual_siliconflow_key"
OPENAI_BASE_URL = "https://api.siliconflow.cn/v1"

# Stripe (replace with your real keys)
STRIPE_SECRET_KEY = "sk_live_YOUR_LIVE_KEY"
STRIPE_PREMIUM_PRICE_ID = "price_YOUR_PREMIUM_ID"
STRIPE_PRO_PRICE_ID = "price_YOUR_PRO_ID"
STRIPE_SINGLE_PRICE_ID = "price_YOUR_SINGLE_ID"

# PayPal (replace with your real IDs)
PAYPAL_CLIENT_ID = "YOUR_PAYPAL_CLIENT_ID"
PAYPAL_CLIENT_SECRET = "YOUR_PAYPAL_SECRET"
PAYPAL_PREMIUM_PLAN_ID = "P-YOUR_PREMIUM_PLAN"
PAYPAL_PRO_PLAN_ID = "P-YOUR_PRO_PLAN"

# App URL (get this after deployment)
APP_URL = "https://your-app-name.streamlit.app"
```

### 4. Post-Deployment Setup

#### A. Configure Webhooks
After deployment, you'll get a URL like `https://your-app.streamlit.app`

**Stripe Webhooks:**
1. Go to Stripe Dashboard > Webhooks
2. Add endpoint: `https://your-app.streamlit.app/webhook/stripe`
3. Select events: `checkout.session.completed`, `customer.subscription.deleted`
4. Copy webhook secret to Streamlit secrets

**PayPal Webhooks:**
1. Go to PayPal Developer Dashboard > Webhooks
2. Add webhook: `https://your-app.streamlit.app/webhook/paypal`
3. Select events: `BILLING.SUBSCRIPTION.ACTIVATED`, `PAYMENT.CAPTURE.COMPLETED`

#### B. Test Payment Flow
1. Deploy app with demo mode enabled
2. Test both Stripe and PayPal payments in sandbox mode
3. Verify subscription activation and cancellation
4. Switch to live mode after testing

### 5. Features Available After Deployment

#### 🆓 Free Tier
- 3 resume analyses per session
- Basic PDF reports
- Standard analysis features

#### ⭐ Premium Tier ($9.99/month)
- Unlimited resume analyses
- Job-specific optimization
- Premium report templates
- Email support

#### 🌟 Pro Tier ($19.99/month)
- Everything in Premium
- Cover letter generation
- Interview preparation
- Priority support
- Advanced analytics

### 6. Revenue Streams
- **Monthly Subscriptions**: $9.99 (Premium) / $19.99 (Pro)
- **Pay-per-use**: $2.99 per single analysis
- **Multiple Payment Options**: Stripe + PayPal for maximum conversions

## Next Steps
1. **Create Stripe Products**: Set up the 3 products mentioned above
2. **Create PayPal Plans**: Set up subscription plans in PayPal
3. **Deploy to Streamlit Cloud**: Change main file to `Home.py`
4. **Add Secrets**: Configure all payment credentials
5. **Test & Go Live**: Test payments then switch to live mode

Ready to proceed? Let me know which step you'd like to start with!