# DropCatchDomain - Automated Domain Catching System

A professional domain catching system that monitors domain status and automatically attempts to register domains when they drop.

## 🚀 Features

- **WHOIS Monitoring**: Uses WhoisXML API to check domain status
- **Smart Scheduling**: Calculates drop times based on registrar patterns
- **Multi-Registrar Catching**: Simultaneous attempts with Dynadot and Porkbun
- **Real-time Notifications**: Email and Discord alerts
- **High-frequency Attempts**: 50ms intervals for maximum success rate
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Error Handling**: Robust error handling and retry mechanisms

## 📁 Project Structure

```
DropCatchDomain/
├── domains.txt                 # List of domains to monitor
├── check_status.py            # WHOIS status checker using WhoisXML API
├── scheduler.py               # Cron scheduler for drop timing
├── catcher.py                 # Domain registration catcher
├── notify.py                  # Notification system
├── config.py                  # API keys and configuration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── domain_catcher.log         # Log file (created automatically)
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Set the following environment variables:

```bash
# Required APIs
export WHOISXML_API_KEY="your_whoisxml_key"
export DYNADOT_API_KEY="your_dynadot_key"
export PORKBUN_API_KEY="your_porkbun_key"

# Optional: Email notifications
export EMAIL_USERNAME="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"

# Optional: Discord notifications
export DISCORD_WEBHOOK="your_discord_webhook_url"
```

### 3. Add Domains to Monitor

Edit `domains.txt` and add domains you want to monitor:

```
example1.com
example2.net
valuable-domain.org
test-domain.info
```

### 4. Start Monitoring

```bash
python scheduler.py
```

## 🔧 Configuration

### API Keys Required

| Service | Purpose | Required | Free Tier |
|---------|---------|----------|-----------|
| **WhoisXML API** | Domain status checking | ✅ Yes | 1000 requests/month |
| **Dynadot API** | Primary registration service | ✅ Yes | No |
| **Porkbun API** | Backup registration service | ✅ Yes | No |
| **Email SMTP** | Notifications | ❌ Optional | Yes |
| **Discord Webhook** | Real-time alerts | ❌ Optional | Yes |

### Configuration Options

Edit `config.py` to customize:

```python
# Monitoring Settings
CHECK_INTERVAL = 3600  # 1 hour in seconds
CATCH_INTERVAL = 0.05  # 50ms between registration attempts
DROP_BUFFER_TIME = 300  # 5 minutes before actual drop time

# Registrar-specific drop times (UTC)
REGISTRAR_DROP_TIMES = {
    'godaddy': {'hour': 14, 'minute': 0},
    'namecheap': {'hour': 15, 'minute': 0},
    'network solutions': {'hour': 14, 'minute': 30},
    'enom': {'hour': 14, 'minute': 15},
    'default': {'hour': 14, 'minute': 0}
}
```

## 🔄 Workflow

1. **Monitoring**: `check_status.py` monitors domains every hour
2. **Detection**: When a domain enters `pendingDelete` status, `scheduler.py` calculates drop time
3. **Scheduling**: Domain catch is scheduled for the calculated drop time
4. **Catching**: At drop time, `catcher.py` attempts registration every 50ms
5. **Notification**: `notify.py` sends success/failure alerts

## 📊 Usage Examples

### Check Domain Status

```bash
python check_status.py
```

### Test Notifications

```bash
python notify.py
```

### Manual Domain Catch

```bash
python catcher.py
# Enter domain when prompted
```

### Start Full Monitoring

```bash
python scheduler.py
```

## 📈 Monitoring and Logs

### Log Levels

- `INFO`: General information and status updates
- `WARNING`: Non-critical issues (failed API calls, etc.)
- `ERROR`: Critical errors that need attention

### Log File

All activities are logged to `domain_catcher.log`:

```
2024-01-15 10:30:00 - INFO - Starting domain monitoring...
2024-01-15 10:30:01 - INFO - Checking example1.com...
2024-01-15 10:30:02 - WARNING - 🚨 example1.com is in pendingDelete status!
2024-01-15 10:30:03 - INFO - Scheduling catch for example1.com at 2024-01-20 14:00:00
```

## 🚨 Rate Limits

| API | Limit | Notes |
|-----|-------|-------|
| WhoisXML | 1000 requests/month | Free tier |
| Dynadot | 100 requests/minute | Paid service |
| Porkbun | 100 requests/minute | Paid service |

## 🔒 Security Best Practices

1. **Environment Variables**: Never hardcode API keys in source code
2. **API Key Rotation**: Regularly rotate your API keys
3. **Network Security**: Use HTTPS for all API communications
4. **Logging**: Avoid logging sensitive information
5. **Access Control**: Limit API key permissions to minimum required

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Please configure WHOISXML_API_KEY in environment variables
   ```
   **Solution**: Set the required environment variables

2. **Network Timeouts**
   ```
   Network error checking example.com: timeout
   ```
   **Solution**: Check internet connection and API service status

3. **Rate Limiting**
   ```
   Rate limit exceeded for WhoisXML API
   ```
   **Solution**: Wait for rate limit reset or upgrade API plan

4. **Domain Not Available**
   ```
   Domain example.com is not available for registration
   ```
   **Solution**: Domain may have been caught by someone else

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python scheduler.py
```

## 📝 Legal Notice

⚠️ **Important**: This tool is for educational purposes only. Ensure you have the right to register domains and comply with all applicable laws and registrar terms of service.

### Terms of Service Compliance

- Respect registrar rate limits
- Don't abuse API services
- Follow domain registration policies
- Comply with local laws

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the logs in `domain_catcher.log`
2. Verify API keys are correctly set
3. Ensure all dependencies are installed
4. Check network connectivity
5. Review rate limits and quotas

## 🔮 Future Enhancements

- [ ] Web dashboard for monitoring
- [ ] Database storage for domain history
- [ ] Multiple notification channels (Slack, Telegram)
- [ ] Advanced scheduling algorithms
- [ ] Domain auction integration
- [ ] Bulk domain management
- [ ] API for external integrations

---

**Happy Domain Catching! 🎯**
