import subprocess
import re
import logging
from datetime import datetime
from config import WHOIS_COMMAND, LOG_LEVEL, LOG_FILE

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

class FreeWhoisChecker:
    def __init__(self):
        self.whois_command = WHOIS_COMMAND
        self.timeout = 30  # seconds
        
    def check_domain_status(self, domain):
        """Check domain status using free whois command"""
        try:
            logger.info(f"Checking {domain} using free whois command...")
            
            # Run whois command
            result = subprocess.run(
                [self.whois_command, domain], 
                capture_output=True, 
                text=True, 
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                logger.warning(f"Whois command failed for {domain} (return code: {result.returncode})")
                return None
            
            output = result.stdout.lower()
            
            # Extract domain information
            domain_info = {
                'domain': domain,
                'status': 'unknown',
                'expiry_date': '',
                'registrar': 'unknown',
                'last_updated': datetime.now().isoformat(),
                'source': 'free_whois'
            }
            
            # Check for pending delete status
            pending_statuses = [
                'pendingdelete', 'redemptionperiod', 'pending delete',
                'redemption period', 'clientdeleteprohibited', 'pendingdeleteperiod',
                'redemption', 'pending delete period'
            ]
            
            for status in pending_statuses:
                if status in output:
                    domain_info['status'] = 'pendingDelete'
                    logger.warning(f"🚨 {domain} is in pendingDelete status!")
                    break
            
            # Extract registrar information
            registrar_patterns = [
                r'registrar:\s*(.+)',
                r'registrar name:\s*(.+)',
                r'registrar organization:\s*(.+)',
                r'registrar\s*:\s*(.+)'
            ]
            
            for pattern in registrar_patterns:
                match = re.search(pattern, output, re.IGNORECASE)
                if match:
                    registrar = match.group(1).strip()
                    # Clean up registrar name
                    registrar = re.sub(r'\s+', ' ', registrar)
                    domain_info['registrar'] = registrar
                    break
            
            # Extract expiry date
            expiry_patterns = [
                r'expires?:\s*(.+)',
                r'expiry date:\s*(.+)',
                r'expiration date:\s*(.+)',
                r'expires on:\s*(.+)'
            ]
            
            for pattern in expiry_patterns:
                match = re.search(pattern, output, re.IGNORECASE)
                if match:
                    expiry_date = match.group(1).strip()
                    # Clean up expiry date
                    expiry_date = re.sub(r'\s+', ' ', expiry_date)
                    domain_info['expiry_date'] = expiry_date
                    break
            
            # Check if domain is expired
            if domain_info['expiry_date']:
                try:
                    # Try to parse expiry date
                    expiry_str = domain_info['expiry_date']
                    # Handle common date formats
                    if 'tld' in expiry_str.lower() or 'utc' in expiry_str.lower():
                        # Skip TLD-specific expiry info
                        pass
                    else:
                        # Try to extract date
                        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', expiry_str)
                        if date_match:
                            expiry_date = datetime.fromisoformat(date_match.group(1))
                            if expiry_date < datetime.now():
                                domain_info['status'] = 'expired'
                                logger.info(f"⚠️ {domain} is expired")
                except (ValueError, TypeError):
                    logger.debug(f"Could not parse expiry date for {domain}: {expiry_date}")
            
            logger.info(f"Status for {domain}: {domain_info['status']}")
            return domain_info
            
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout checking {domain} (>{self.timeout}s)")
            return None
        except FileNotFoundError:
            logger.error(f"Whois command not found. Please install whois utility.")
            return None
        except Exception as e:
            logger.error(f"Error checking {domain}: {e}")
            return None
    
    def is_pending_delete(self, domain_info):
        """Check if domain is in pendingDelete status"""
        if not domain_info:
            return False
            
        status = domain_info.get('status', '').lower()
        return status == 'pendingdelete'
    
    def is_expired(self, domain_info):
        """Check if domain is expired"""
        if not domain_info:
            return False
            
        status = domain_info.get('status', '').lower()
        return status == 'expired'
    
    def test_whois_command(self):
        """Test if whois command is available"""
        try:
            result = subprocess.run(
                [self.whois_command, '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("SUCCESS: Whois command is available")
                return True
            else:
                logger.warning("WARNING: Whois command returned non-zero exit code")
                return False
                
        except FileNotFoundError:
            logger.error("FAILED: Whois command not found. Please install whois utility.")
            return False
        except Exception as e:
            logger.error(f"FAILED: Error testing whois command: {e}")
            return False

if __name__ == "__main__":
    checker = FreeWhoisChecker()
    
    # Test whois command availability
    if not checker.test_whois_command():
        print("Please install whois utility:")
        print("Windows: Install Git Bash or WSL")
        print("Linux: sudo apt-get install whois")
        print("macOS: brew install whois")
        exit(1)
    
    # Test with a domain
    test_domain = input("Enter domain to test: ").strip()
    if test_domain:
        result = checker.check_domain_status(test_domain)
        if result:
            print(f"\nDomain: {result['domain']}")
            print(f"Status: {result['status']}")
            print(f"Registrar: {result['registrar']}")
            print(f"Expiry: {result['expiry_date']}")
            print(f"Source: {result['source']}")
        else:
            print("Failed to check domain status")
