import requests
import time
import threading
import logging
from datetime import datetime, timedelta
from config import (
    PORKBUN_API_KEY, PORKBUN_SECRET_KEY, DYNADOT_API_KEY, CATCH_INTERVAL, 
    MAX_RETRY_ATTEMPTS, RETRY_DELAY, LOG_LEVEL, LOG_FILE
)
from notify import NotificationManager

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

class DomainCatcher:
    def __init__(self):
        self.porkbun_key = PORKBUN_API_KEY
        self.porkbun_secret = PORKBUN_SECRET_KEY
        self.porkbun_url = "https://api.porkbun.com/api/json/v3"
        self.dynadot_key = DYNADOT_API_KEY
        
        # Create session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DomainCatcher/1.0'
        })
        
        # Track registration attempts
        self.attempts = {}
        self.results = {}
        
        # Import Dynadot API
        try:
            from dynadot_api import DynadotAPI
            self.dynadot_api = DynadotAPI()
            logger.info("Dynadot API initialized successfully")
        except ImportError as e:
            logger.error(f"Failed to import Dynadot API: {e}")
            self.dynadot_api = None
        
        # Initialize notification manager
        self.notifier = NotificationManager()
    
    def check_availability(self, domain):
        """Check if domain is available for registration using Dynadot API"""
        try:
            # Use Dynadot API for availability check
            if self.dynadot_api:
                available = self.dynadot_api.check_domain_availability(domain)
                logger.info(f"Availability check for {domain}: {'Available' if available else 'Not Available'}")
                return available
            else:
                logger.warning(f"Dynadot API not available for {domain}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking availability for {domain}: {e}")
            return False
    
    
    def register_with_dynadot(self, domain):
        """Register domain using Dynadot API"""
        try:
            if not self.dynadot_api:
                logger.error("Dynadot API not available")
                return False, "Dynadot API not initialized"
            
            if not self.dynadot_key:
                logger.error("Dynadot API key not configured")
                return False, "Dynadot API key not configured"
            
            logger.info(f"Attempting to register {domain} via Dynadot API")
            success, message = self.dynadot_api.register_domain(domain)
            
            if success:
                logger.info(f"SUCCESS: Domain {domain} registered via Dynadot")
                return True, message
            else:
                logger.error(f"FAILED: Domain {domain} registration failed via Dynadot: {message}")
                return False, message
                
        except Exception as e:
            logger.error(f"Error registering {domain} with Dynadot: {e}")
            return False, str(e)
    
    def register_with_porkbun(self, domain):
        """Manual registration guidance since Porkbun API doesn't support domain registration"""
        try:
            logger.info(f"Porkbun API doesn't support domain registration. Manual registration required for {domain}")
            
            # Provide manual registration instructions
            message = f"""
            MANUAL REGISTRATION REQUIRED:
            
            Domain: {domain}
            Registrar: Porkbun
            
            Steps:
            1. Go to https://porkbun.com
            2. Search for '{domain}'
            3. Add to cart and complete registration
            4. Use your credit card for payment
            
            Note: Porkbun API only supports domain management after registration,
            not the initial domain registration process.
            """
            
            logger.info(message)
            return False, "Manual registration required - Porkbun API doesn't support domain registration"
            
        except Exception as e:
            logger.error(f"Error with manual registration guidance for {domain}: {e}")
            return False, str(e)
    
    def attempt_registration(self, domain):
        """Attempt to register domain with available registrars"""
        logger.info(f"Starting registration attempt for {domain}")
        
        # Try Dynadot first (primary registrar)
        if self.dynadot_api and self.dynadot_key:
            logger.info(f"Attempting registration with Dynadot for {domain}")
            success, message = self.register_with_dynadot(domain)
            
            if success:
                logger.info(f"SUCCESS: Successfully registered {domain} with Dynadot")
                self.notifier.send_success_notification(domain, message)
                return True, f"Dynadot: {message}"
            else:
                logger.warning(f"FAILED: Dynadot registration failed for {domain}: {message}")
                self.notifier.send_failure_notification(domain, message)
        
        # Fallback to Porkbun (manual registration)
        logger.info(f"Falling back to Porkbun manual registration for {domain}")
        success, message = self.register_with_porkbun(domain)
        
        if success:
            logger.info(f"SUCCESS: Manual registration guidance provided for {domain}")
            self.notifier.send_notification("Manual Registration Required", f"Domain {domain} requires manual registration via Porkbun website", "warning")
            return True, f"Porkbun: {message}"
        else:
            logger.warning(f"FAILED: No registration method available for {domain}")
            self.notifier.send_failure_notification(domain, "All registration methods failed")
            return False, f"All methods failed: {message}"
    
    def catch_domain(self, domain, max_duration_minutes=5):
        """Attempt to catch a domain using high-frequency attempts"""
        logger.info(f"Starting catch attempt for {domain}")
        
        start_time = datetime.now()
        max_duration = timedelta(minutes=max_duration_minutes)
        attempts = 0
        last_availability_check = datetime.now()
        
        # Initialize tracking
        self.attempts[domain] = 0
        self.results[domain] = {'success': False, 'message': '', 'attempts': 0}
        
        while datetime.now() - start_time < max_duration:
            attempts += 1
            self.attempts[domain] = attempts
            
            # Check availability every 10 attempts to avoid rate limiting
            if attempts % 10 == 0 or datetime.now() - last_availability_check > timedelta(seconds=30):
                if self.check_availability(domain):
                    logger.info(f"Domain {domain} is available! Attempting registration...")
                    
                    success, message = self.attempt_registration(domain)
                    
                    if success:
                        self.results[domain] = {
                            'success': True,
                            'message': message,
                            'attempts': attempts
                        }
                        logger.info(f"🎉 Successfully caught {domain} after {attempts} attempts!")
                        return True
                    else:
                        logger.warning(f"Registration failed for {domain}: {message}")
                
                last_availability_check = datetime.now()
            
            # Wait before next attempt
            time.sleep(CATCH_INTERVAL)
            
            # Log progress every 1000 attempts
            if attempts % 1000 == 0:
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.info(f"Attempt {attempts}: {elapsed:.1f}s elapsed for {domain}")
        
        # Final attempt
        logger.info(f"Final attempt for {domain}...")
        if self.check_availability(domain):
            success, message = self.attempt_registration(domain)
            if success:
                self.results[domain] = {
                    'success': True,
                    'message': message,
                    'attempts': attempts
                }
                return True
        
        # Update final result
        self.results[domain] = {
            'success': False,
            'message': f"Failed after {attempts} attempts in {max_duration_minutes} minutes",
            'attempts': attempts
        }
        
        logger.warning(f"Failed to catch {domain} after {attempts} attempts")
        return False
    
    def get_catch_stats(self, domain):
        """Get statistics for a domain catch attempt"""
        return self.results.get(domain, {'success': False, 'message': 'No attempts made', 'attempts': 0})
    
    def cleanup(self):
        """Clean up resources"""
        self.session.close()

if __name__ == "__main__":
    catcher = DomainCatcher()
    
    # Check if API keys are configured
    if not DYNADOT_API_KEY:
        logger.error("Please configure DYNADOT_API_KEY in environment variables")
        logger.info("Get your Dynadot API key from: https://www.dynadot.com/domain/api")
        exit(1)
    
    try:
        domain = input("Enter domain to catch: ").strip()
        if not domain:
            print("No domain provided")
            exit(1)
        
        print(f"Starting catch attempt for {domain}...")
        success = catcher.catch_domain(domain)
        
        stats = catcher.get_catch_stats(domain)
        print(f"\nCatch result: {'Success' if success else 'Failed'}")
        print(f"Attempts: {stats['attempts']}")
        print(f"Message: {stats['message']}")
        
    except KeyboardInterrupt:
        print("\nCatch attempt interrupted by user")
    finally:
        catcher.cleanup()
