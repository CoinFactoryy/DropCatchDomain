# Railway Deployment Instructions

## ✅ Files Created
- `.env.example` - Template for environment variables
- `.env` - Your actual environment variables (git-ignored)
- `railway.json` - Railway configuration
- `Procfile` - Process definition for Railway
- `railway_setup.md` - Detailed setup guide

## 🚀 Quick Deployment Steps

### 1. Fill in your .env file
Edit `.env` and replace the placeholder values:
```
DYNADOT_API_KEY=your_actual_dynadot_api_key
PORKBUN_API_KEY=your_actual_porkbun_api_key
PORKBUN_SECRET_KEY=your_actual_porkbun_secret_key
DISCORD_WEBHOOK=your_actual_discord_webhook_url
```

### 2. Push to GitHub
```bash
git add .
git commit -m "Add Railway deployment files"
git push origin main
```

### 3. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project from GitHub repo
4. Select your repository
5. Railway will auto-deploy

### 4. Set Environment Variables in Railway
In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add each environment variable from your `.env` file

## 📊 Monitoring Settings
- **Check Interval**: 20 minutes (1200 seconds)
- **Domains**: 20 domains from domains.txt
- **Notifications**: Discord webhook
- **Database**: SQLite (domains.db)

## 🔧 Configuration Files
- `config.py` - Main configuration (updated for 20-minute intervals)
- `requirements.txt` - Python dependencies
- `domains.txt` - List of domains to monitor

## 📝 Next Steps
1. Fill in your `.env` file with real API keys
2. Push to GitHub
3. Deploy on Railway
4. Set environment variables in Railway dashboard
5. Monitor your deployment

## 🆓 Free Tier Limits
- 500 hours/month
- $5 credit monthly
- Perfect for domain monitoring

Your system is now ready for Railway deployment!
