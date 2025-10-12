import time
import logging
from datetime import datetime
from config import DOMAINS_FILE, LOG_LEVEL, LOG_FILE, USE_FREE_WHOIS
from free_whois_checker import FreeWhoisChecker
from dynadot_api import DynadotAPI

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DomainStatusChecker:
    def __init__(self):
        self.free_checker = FreeWhoisChecker()
        self.dynadot_api = DynadotAPI()
        self.domains_cache = {}  # Cache for domain status
    
    def check_domain_status(self, domain):
        """Check domain status using Dynadot API or free whois command"""
        try:
            # Check cache first
            if domain in self.domains_cache:
                cached_info = self.domains_cache[domain]
                # Use cache if less than 1 hour old
                if datetime.now().timestamp() - datetime.fromisoformat(cached_info['last_updated']).timestamp() < 3600:
                    logger.debug(f"Using cached data for {domain}")
                    return cached_info
            
            # Use Dynadot API first (more reliable)
            if not USE_FREE_WHOIS:
                logger.info(f"Checking {domain} using Dynadot API")
                available = self.dynadot_api.check_domain_availability(domain)
                
                domain_info = {
                    'domain': domain,
                    'status': 'available' if available else 'registered',
                    'expiry_date': '',
                    'registrar': 'unknown',
                    'last_updated': datetime.now().isoformat(),
                    'source': 'dynadot_api'
                }
                
                if domain_info:
                    # Cache the result
                    self.domains_cache[domain] = domain_info
                    logger.info(f"Status for {domain}: {domain_info['status']}")
                
                return domain_info
            else:
                # Fallback to free whois checker
                domain_info = self.free_checker.check_domain_status(domain)
                
                if domain_info:
                    # Cache the result
                    self.domains_cache[domain] = domain_info
                    logger.info(f"Status for {domain}: {domain_info['status']}")
                
                return domain_info
            
        except Exception as e:
            logger.error(f"Error checking {domain}: {e}")
            return None
    
    def is_pending_delete(self, domain_info):
        """Check if domain is in pendingDelete status"""
        return self.free_checker.is_pending_delete(domain_info)
    
    def is_expired(self, domain_info):
        """Check if domain is expired"""
        return self.free_checker.is_expired(domain_info)
    
    def load_domains(self):
        """Load domains from domains.txt"""
        try:
            with open(DOMAINS_FILE, 'r', encoding='utf-8') as f:
                domains = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            logger.info(f"Loaded {len(domains)} domains from {DOMAINS_FILE}")
            return domains
        except FileNotFoundError:
            logger.error(f"Error: {DOMAINS_FILE} not found")
            return []
        except Exception as e:
            logger.error(f"Error loading domains: {e}")
            return []
    
    def monitor_all_domains(self):
        """Monitor all domains and return pendingDelete ones"""
        domains = self.load_domains()
        if not domains:
            logger.warning("No domains to monitor")
            return []
            
        pending_delete = []
        expired_domains = []
        
        for domain in domains:
            logger.info(f"Checking {domain}...")
            domain_info = self.check_domain_status(domain)
            
            if domain_info:
                if self.is_pending_delete(domain_info):
                    pending_delete.append(domain_info)
                    logger.warning(f"ALERT: {domain} is in pendingDelete status!")
                elif self.is_expired(domain_info):
                    expired_domains.append(domain_info)
                    logger.info(f"WARNING: {domain} is expired")
                else:
                    logger.info(f"SUCCESS: {domain} status: {domain_info['status']}")
            else:
                logger.error(f"FAILED: Failed to check {domain}")
            
            # Rate limiting - be respectful to the API
            time.sleep(1)
        
        # Log summary
        logger.info(f"Monitoring complete: {len(pending_delete)} pendingDelete, {len(expired_domains)} expired")
        
        return pending_delete
    
    def get_domain_details(self, domain):
        """Get detailed information about a specific domain"""
        return self.check_domain_status(domain)

if __name__ == "__main__":
    checker = DomainStatusChecker()
    
    # Test Dynadot API availability
    if not checker.dynadot_api.test_api_connection():
        logger.error("Please check your Dynadot API key and internet connection")
        exit(1)
    
    pending_domains = checker.monitor_all_domains()
    
    if pending_domains:
        print(f"\nALERT: Found {len(pending_domains)} domains in pendingDelete:")
        for domain_info in pending_domains:
            print(f"- {domain_info['domain']}: {domain_info['status']}")
            print(f"  Registrar: {domain_info['registrar']}")
            print(f"  Expiry: {domain_info['expiry_date']}")
            print(f"  Source: {domain_info['source']}")
            print()
    else:
        print("SUCCESS: No domains in pendingDelete status found.")
