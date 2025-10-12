# Render Deployment Guide

## 🚀 Why Render?
- **750 hours/month free** (vs Railway's 500 hours)
- **Automatic GitHub sync**
- **Python support**
- **Easy setup**
- **No sleep mode** for web services

## 📁 Files Created
- `render.yaml` - Render configuration
- `health_server.py` - Health check server (already exists)
- `requirements.txt` - Python dependencies (already exists)

## 🔧 Configuration
- **Service Type**: Web service
- **Runtime**: Python
- **Plan**: Free
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python health_server.py`
- **Health Check**: `/health` endpoint

## 🚀 Deployment Steps

### Step 1: Sign up for Render
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Authorize Render to access your repositories

### Step 2: Deploy from GitHub
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Select your domain monitoring repository
5. Click "Connect"

### Step 3: Configure Service
Render will auto-detect your `render.yaml` configuration:
- **Name**: domain-monitor
- **Environment**: Python
- **Plan**: Free
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python health_server.py`

### Step 4: Set Environment Variables
In Render dashboard, go to Environment tab and add:
```
DYNADOT_API_KEY=7O8g6F6T9O6i6N657o8O8f7Tb7HO6X9L9H8W9G7e7q9W8d
PORKBUN_API_KEY=your_actual_porkbun_api_key
PORKBUN_SECRET_KEY=your_actual_porkbun_secret_key
DISCORD_WEBHOOK=https://discord.com/api/webhooks/1426753499663831190/hxkcuWmGah8uEStf3nB7O73PCkA-Af-UisOU5bf0op56yKaUbYVhVR-BpAQl3Qy2g9zp
LOG_LEVEL=INFO
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Check logs for any errors
4. Test health check endpoint

## 📊 What to Expect
- ✅ **750 hours/month free** (vs Railway's 500)
- ✅ **Automatic GitHub sync**
- ✅ **No sleep mode** (always running)
- ✅ **Health check at `/health`**
- ✅ **Domain monitoring every 20 minutes**
- ✅ **Discord notifications**

## 🔧 Configuration Details

### render.yaml
```yaml
services:
  - type: web
    name: domain-monitor
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python health_server.py
    healthCheckPath: /health
    autoDeploy: true
```

### Environment Variables
- `DYNADOT_API_KEY` - Your Dynadot API key
- `PORKBUN_API_KEY` - Your Porkbun API key (optional)
- `PORKBUN_SECRET_KEY` - Your Porkbun secret key (optional)
- `DISCORD_WEBHOOK` - Your Discord webhook URL
- `LOG_LEVEL` - Logging level (INFO)

## 🆓 Free Tier Benefits
- **750 hours/month** (50% more than Railway)
- **No sleep mode** for web services
- **Automatic deployments**
- **GitHub integration**
- **Custom domains**

## 📝 Adding New Domains
1. Edit `domains.txt` on GitHub
2. Push changes to GitHub
3. Render automatically redeploys
4. New domains are monitored automatically

## 🔍 Monitoring
- **Logs**: Available in Render dashboard
- **Health Check**: `https://your-app.onrender.com/health`
- **Status**: Always running (no sleep mode)

## 🚀 Next Steps
1. Sign up for Render
2. Connect GitHub repository
3. Deploy web service
4. Set environment variables
5. Test deployment
6. Monitor domain monitoring

## ✅ Success Indicators
- Deployment completes successfully
- Health check returns 200 OK
- Domain monitoring starts
- Discord notifications work
- Logs show activity

Your domain monitoring system is now ready for Render deployment!
