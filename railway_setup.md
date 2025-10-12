# Railway Deployment Guide

## Step 1: Sign up for Railway
1. Go to [railway.app](https://railway.app)
2. Click "Sign Up"
3. Choose "Sign up with GitHub"
4. Authorize Railway to access your GitHub account

## Step 2: Deploy from GitHub
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your domain monitoring repository
4. Click "Deploy"

## Step 3: Set Environment Variables
In Railway dashboard, go to your project → Variables tab and add:

```
DYNADOT_API_KEY=your_actual_dynadot_api_key
PORKBUN_API_KEY=your_actual_porkbun_api_key
PORKBUN_SECRET_KEY=your_actual_porkbun_secret_key
DISCORD_WEBHOOK=your_actual_discord_webhook_url
LOG_LEVEL=INFO
```

## Step 4: Monitor Deployment
1. Check Railway dashboard for deployment status
2. View logs to ensure everything is working
3. Test your domain monitoring

## Step 5: Verify Environment Variables
Make sure all required environment variables are set:
- DYNADOT_API_KEY
- PORKBUN_API_KEY
- PORKBUN_SECRET_KEY
- DISCORD_WEBHOOK

## Troubleshooting
- Check Railway logs for errors
- Verify environment variables are set correctly
- Ensure all dependencies are in requirements.txt
- Check that domains.txt contains your domains

## Free Tier Limits
- 500 hours/month
- $5 credit monthly
- May require payment method for verification
