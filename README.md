# Domain Monitor - Render Deployment

Automated domain monitoring system deployed on Render with 750 hours/month free.

## 🚀 Quick Deploy to Render

1. **Sign up**: Go to [render.com](https://render.com) and sign up with GitHub
2. **Deploy**: Click "New +" → "Web Service" → Connect your repository
3. **Configure**: Render auto-detects `render.yaml` configuration
4. **Set Environment Variables**: Add your API keys in Render dashboard
5. **Deploy**: Click "Create Web Service"

## 📁 Project Structure

```
├── health_server.py      # Flask server with health check
├── scheduler.py          # Domain monitoring scheduler
├── config.py            # Configuration settings
├── dynadot_api.py       # Dynadot API integration
├── notify.py            # Discord notifications
├── database.py          # SQLite database
├── domains.txt          # Domains to monitor
├── requirements.txt     # Python dependencies
├── render.yaml          # Render configuration
└── .env                 # Environment variables
```

## 🔧 Configuration

### Environment Variables
Set these in Render dashboard:
```
DYNADOT_API_KEY=your_dynadot_api_key
PORKBUN_API_KEY=your_porkbun_api_key
PORKBUN_SECRET_KEY=your_porkbun_secret_key
DISCORD_WEBHOOK=your_discord_webhook_url
LOG_LEVEL=INFO
```

### Monitoring Settings
- **Check Interval**: 20 minutes
- **Domains**: Loaded from `domains.txt`
- **Notifications**: Discord webhook
- **Database**: SQLite

## 📊 Features

- ✅ **750 hours/month free** on Render
- ✅ **No sleep mode** (always running)
- ✅ **Automatic GitHub sync**
- ✅ **Health check endpoint** (`/health`)
- ✅ **Domain monitoring** every 20 minutes
- ✅ **Discord notifications**
- ✅ **Dynadot API integration**

## 🔄 Adding New Domains

1. Edit `domains.txt` on GitHub
2. Push changes to GitHub
3. Render automatically redeploys
4. New domains are monitored automatically

## 📝 Usage

- **Health Check**: `https://your-app.onrender.com/health`
- **Monitoring**: Automatic every 20 minutes
- **Notifications**: Discord webhook
- **Logs**: Available in Render dashboard

## 🆓 Free Tier Benefits

- **750 hours/month** (50% more than Railway)
- **No sleep mode** for web services
- **Automatic deployments**
- **GitHub integration**
- **Custom domains**

## 🚀 Ready to Deploy!

Your domain monitoring system is fully configured for Render deployment.

**Go to [render.com](https://render.com) and deploy now!**