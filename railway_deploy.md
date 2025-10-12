# Railway Deployment Instructions

## ✅ Fixed Issues
- Removed health check from railway.json
- Updated monitoring interval to 20 minutes
- Created environment variable templates

## 🚀 Deployment Steps

### Step 1: Push Changes to GitHub
```bash
git add .
git commit -m "Fix Railway deployment - remove health check"
git push origin main
```

### Step 2: Redeploy on Railway
1. Go to your Railway project
2. Click "Redeploy" or "Deploy"
3. Wait for deployment to complete

### Step 3: Set Environment Variables
In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add these variables:

```
DYNADOT_API_KEY=your_actual_dynadot_api_key
PORKBUN_API_KEY=your_actual_porkbun_api_key
PORKBUN_SECRET_KEY=your_actual_porkbun_secret_key
DISCORD_WEBHOOK=your_actual_discord_webhook_url
LOG_LEVEL=INFO
```

### Step 4: Monitor Deployment
1. Check "Logs" tab
2. Verify scheduler.py starts successfully
3. Look for domain monitoring activity

## 📊 What to Expect
- ✅ Deployment succeeds (no health check errors)
- ✅ Domain monitoring starts automatically
- ✅ Checks 20 domains every 20 minutes
- ✅ Sends Discord notifications
- ✅ Logs all activity

## 🔧 Configuration
- **Check Interval**: 20 minutes (1200 seconds)
- **Domains**: Loaded from domains.txt
- **Notifications**: Discord webhook
- **Database**: SQLite (domains.db)

## 📝 Next Steps
1. Push changes to GitHub
2. Redeploy on Railway
3. Set environment variables
4. Monitor logs
5. Test notifications

## 🆓 Free Tier
- 500 hours/month
- Perfect for domain monitoring
- No billing required

Your deployment should now work correctly!
