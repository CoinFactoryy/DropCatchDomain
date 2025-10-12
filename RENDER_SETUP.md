# Render Setup - Step by Step

## 🎯 Goal
Deploy your domain monitoring system to Render with 750 hours/month free.

## 📋 Prerequisites
- ✅ GitHub repository with your code
- ✅ Domain monitoring system ready
- ✅ API keys configured
- ✅ Discord webhook ready

## 🚀 Step 1: Sign up for Render
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your repositories
5. Complete account setup

## 🔗 Step 2: Connect Repository
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Click "Connect GitHub"
4. Select your domain monitoring repository
5. Click "Connect"

## ⚙️ Step 3: Configure Service
Render will auto-detect your configuration:

### Basic Settings
- **Name**: domain-monitor
- **Environment**: Python
- **Plan**: Free
- **Region**: Choose closest to you

### Build & Deploy
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python health_server.py`
- **Health Check Path**: `/health`

### Advanced Settings
- **Auto-Deploy**: Yes
- **Branch**: main
- **Root Directory**: (leave empty)

## 🔑 Step 4: Set Environment Variables
In the Environment tab, add these variables:

```
DYNADOT_API_KEY=7O8g6F6T9O6i6N657o8O8f7Tb7HO6X9L9H8W9G7e7q9W8d
PORKBUN_API_KEY=your_actual_porkbun_api_key
PORKBUN_SECRET_KEY=your_actual_porkbun_secret_key
DISCORD_WEBHOOK=https://discord.com/api/webhooks/1426753499663831190/hxkcuWmGah8uEStf3nB7O73PCkA-Af-UisOU5bf0op56yKaUbYVhVR-BpAQl3Qy2g9zp
LOG_LEVEL=INFO
```

## 🚀 Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Check the logs for any errors
4. Note your app URL (e.g., `https://domain-monitor.onrender.com`)

## ✅ Step 6: Test Deployment
1. **Health Check**: Visit `https://your-app.onrender.com/health`
2. **Logs**: Check Render dashboard logs
3. **Discord**: Wait for first notification (20 minutes)
4. **Monitoring**: Verify domain monitoring is working

## 📊 Expected Results
- ✅ **Deployment succeeds**
- ✅ **Health check returns 200 OK**
- ✅ **Domain monitoring starts**
- ✅ **Discord notifications work**
- ✅ **Logs show activity**

## 🔧 Troubleshooting

### Common Issues
1. **Build fails**: Check `requirements.txt`
2. **Start fails**: Check `health_server.py`
3. **Health check fails**: Check Flask server
4. **Environment variables**: Verify all keys are set

### Solutions
1. **Check logs** in Render dashboard
2. **Verify environment variables**
3. **Test locally** first
4. **Check GitHub repository** for latest code

## 📈 Benefits of Render
- **750 hours/month free** (vs Railway's 500)
- **No sleep mode** for web services
- **Automatic GitHub sync**
- **Easy setup**
- **Reliable hosting**

## 🔄 Adding New Domains
1. Edit `domains.txt` on GitHub
2. Push changes to GitHub
3. Render automatically redeploys
4. New domains are monitored automatically

## 📝 Next Steps
1. Sign up for Render
2. Connect GitHub repository
3. Deploy web service
4. Set environment variables
5. Test deployment
6. Monitor domain monitoring

## 🎉 Success!
Your domain monitoring system is now running on Render with:
- 750 hours/month free
- Automatic GitHub sync
- No sleep mode
- Health check endpoint
- Discord notifications

Ready to deploy!
