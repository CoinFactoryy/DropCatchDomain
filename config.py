import os
from datetime import timedelta

# Load environment variables from .env file (optional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not available, use system environment variables

# Beginner Combo Configuration
# Free WHOIS monitoring + Porkbun registration + Discord notifications

# WHOIS Configuration (Dynadot API)
USE_FREE_WHOIS = False  # Use Dynadot API instead of system whois command
WHOIS_COMMAND = 'whois'  # Fallback system command

# Registration APIs
PORKBUN_API_KEY = os.getenv('PORKBUN_API_KEY')
PORKBUN_SECRET_KEY = os.getenv('PORKBUN_SECRET_KEY')

# Dynadot API for domain registration (primary)
DYNADOT_API_KEY = os.getenv('DYNADOT_API_KEY')
DYNADOT_API_URL = 'https://api.dynadot.com/api3.json'

# Monitoring Settings
CHECK_INTERVAL = 1200  # 20 minutes in seconds
CATCH_INTERVAL = 0.05  # 50ms between registration attempts
DROP_BUFFER_TIME = 300  # 5 minutes before actual drop time

# Notification Settings (Discord focus for beginners)
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

# Optional: Email notifications (can be added later)
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

# Target domains
DOMAINS_FILE = 'domains.txt'

# Database (SQLite for beginners)
DATABASE_FILE = 'domains.db'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'domain_catcher.log'

# Registrar-specific drop times (UTC)
REGISTRAR_DROP_TIMES = {
    'godaddy': {'hour': 14, 'minute': 0},
    'namecheap': {'hour': 15, 'minute': 0},
    'network solutions': {'hour': 14, 'minute': 30},
    'enom': {'hour': 14, 'minute': 15},
    'default': {'hour': 14, 'minute': 0}
}

# Retry settings
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

# Success criteria
SUCCESS_THRESHOLD = 0.8  # 80% success rate threshold
