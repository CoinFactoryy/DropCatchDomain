# 🚀 Beginner Combo Setup Guide

This guide will help you set up the **Beginner Combo** domain catching system with minimal cost and maximum simplicity.

## 📋 What You'll Get

- **Free WHOIS monitoring** using system commands
- **Porkbun API** for domain registration ($5-15/month)
- **Discord notifications** (free)
- **SQLite database** for tracking (free)
- **Total cost: ~$10-20/month**

## 🛠️ Step-by-Step Setup

### Step 1: Install Prerequisites

#### Windows
```bash
# Install Git Bash (includes whois command)
# Download from: https://git-scm.com/download/win

# Or install WSL (Windows Subsystem for Linux)
wsl --install
```

#### Linux
```bash
sudo apt-get update
sudo apt-get install whois python3 python3-pip
```

#### macOS
```bash
brew install whois python3
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Get Dynadot API Key (Primary)

1. **Sign up at Dynadot**: https://www.dynadot.com/
2. **Go to API Settings**: Tools → API
3. **Generate API Key**: Create new API key
4. **Copy your API key**

### Step 4: Get Porkbun API Keys (Optional)

1. **Sign up at Porkbun**: https://porkbun.com/
2. **Go to API Settings**: Account → API Settings
3. **Generate API Key**: Create new API key
4. **Copy your keys**:
   - API Key
   - Secret Key

### Step 5: Set Up Discord Webhook

1. **Create Discord Server** (if you don't have one)
2. **Go to Server Settings** → Integrations → Webhooks
3. **Create New Webhook**:
   - Name: "Domain Catcher"
   - Channel: Choose your notification channel
4. **Copy Webhook URL**

### Step 6: Configure Environment Variables

Create a `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit with your actual values
notepad .env
```

Fill in your `.env` file:

```env
# Required: Dynadot API Key (Primary)
DYNADOT_API_KEY=your_actual_dynadot_api_key_here

# Optional: Porkbun API Keys (for domain management)
PORKBUN_API_KEY=your_actual_api_key_here
PORKBUN_SECRET_KEY=your_actual_secret_key_here

# Required: Discord Webhook
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your_webhook_url_here

# Optional: Email (can be added later)
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Step 6: Add Domains to Monitor

Edit `domains.txt`:

```bash
notepad domains.txt
```

Add your target domains:

```
example1.com
example2.net
valuable-domain.org
my-target-domain.com
```

### Step 7: Test the System

#### Test WHOIS Command
```bash
python free_whois_checker.py
```

#### Test Notifications
```bash
python notify.py
```

#### Test Domain Status Checking
```bash
python check_status.py
```

#### Test Database
```bash
python database.py
```

### Step 8: Start Monitoring

```bash
python scheduler.py
```

## 🔧 Configuration Options

### Basic Settings (config.py)

```python
# Monitoring frequency
CHECK_INTERVAL = 3600  # Check every hour

# Catch attempt frequency
CATCH_INTERVAL = 0.05  # 50ms between attempts

# Drop time buffer
DROP_BUFFER_TIME = 300  # 5 minutes before drop
```

### Advanced Settings

```python
# Logging level
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# Database cleanup
CLEANUP_DAYS = 30  # Keep records for 30 days
```

## 📊 Monitoring Your System

### Check Logs
```bash
# View recent logs
tail -f domain_catcher.log

# Search for specific domains
grep "example.com" domain_catcher.log
```

### Database Queries
```bash
# View all domains
sqlite3 domains.db "SELECT * FROM domains;"

# View catch attempts
sqlite3 domains.db "SELECT * FROM catch_attempts;"

# View notifications
sqlite3 domains.db "SELECT * FROM notifications;"
```

### System Status
```bash
# Check if system is running
ps aux | grep scheduler.py

# Check database size
ls -lh domains.db
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "Whois command not found"
```bash
# Windows: Install Git Bash or WSL
# Linux: sudo apt-get install whois
# macOS: brew install whois
```

#### 2. "Porkbun API key not configured"
```bash
# Check your .env file
cat .env | grep PORKBUN

# Test API key
curl -X POST "https://porkbun.com/api/json/v3/domain/check" \
  -H "Content-Type: application/json" \
  -d '{"apikey":"YOUR_KEY","secretapikey":"YOUR_SECRET","domain":"test.com"}'
```

#### 3. "Discord webhook not working"
```bash
# Test webhook
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"Test message"}'
```

#### 4. "Database errors"
```bash
# Recreate database
rm domains.db
python database.py
```

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python scheduler.py
```

## 📈 Usage Examples

### Monitor Specific Domain
```bash
python check_status.py
# Enter domain when prompted
```

### Manual Domain Catch
```bash
python catcher.py
# Enter domain when prompted
```

### View System Stats
```bash
python -c "from database import DomainDatabase; db = DomainDatabase(); print(db.get_stats())"
```

## 🔄 Maintenance

### Daily Tasks
- Check logs for errors
- Monitor Discord notifications
- Verify domain status updates

### Weekly Tasks
- Review catch attempts
- Clean up old database records
- Update domain list

### Monthly Tasks
- Review API usage and costs
- Update system dependencies
- Backup database

## 💰 Cost Breakdown

| Service | Cost | Purpose |
|---------|------|---------|
| Porkbun API | $5-15/month | Domain registration |
| Discord | Free | Notifications |
| WHOIS | Free | Domain monitoring |
| Database | Free | Data storage |
| **Total** | **$5-15/month** | **Complete system** |

## 🆘 Support

### Getting Help

1. **Check logs**: `tail -f domain_catcher.log`
2. **Test components**: Run individual Python files
3. **Verify configuration**: Check `.env` file
4. **Check prerequisites**: Ensure whois command works

### Common Commands

```bash
# Check system status
python -c "import sys; print('Python:', sys.version)"

# Test whois
whois google.com

# Test Porkbun API
python -c "from catcher import DomainCatcher; c = DomainCatcher(); print(c.check_availability('test.com'))"

# Test Discord
python notify.py
```

## 🎯 Next Steps

Once you're comfortable with the beginner combo:

1. **Add Dynadot API** for backup registration
2. **Add email notifications** for redundancy
3. **Upgrade to paid WHOIS APIs** for better data
4. **Add web dashboard** for easier management
5. **Scale up** to more domains

## 📝 Notes

- **Start small**: Monitor 5-10 domains initially
- **Test thoroughly**: Verify each component works
- **Monitor costs**: Keep track of API usage
- **Backup regularly**: Save your database and config
- **Stay updated**: Keep dependencies current

---

**Happy Domain Catching! 🎯**

For questions or issues, check the logs first, then test individual components.
