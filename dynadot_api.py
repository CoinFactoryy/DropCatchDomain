#!/usr/bin/env python3
"""
Dynadot API integration for domain registration
"""
import requests
import logging
from config import DYNADOT_API_KEY, DYNADOT_API_URL, LOG_LEVEL, LOG_FILE

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

class DynadotAPI:
    def __init__(self):
        self.api_key = DYNADOT_API_KEY
        self.api_url = DYNADOT_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DomainCatcher/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def check_domain_availability(self, domain):
        """Check if domain is available for registration"""
        try:
            data = {
                'key': self.api_key,
                'command': 'search',
                'domain0': domain
            }
            
            logger.info(f"Checking availability for {domain} via Dynadot API")
            response = self.session.get(self.api_url, params=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"Dynadot availability response: {result}")
            
            # Parse Dynadot response
            if 'SearchResponse' in result:
                search_response = result['SearchResponse']
                if 'ResponseCode' in search_response and search_response['ResponseCode'] == '0':
                    if 'SearchResults' in search_response:
                        search_results = search_response['SearchResults']
                        if isinstance(search_results, list) and len(search_results) > 0:
                            # Handle array format: [{'DomainName': 'domain.com', 'Available': 'yes'}]
                            domain_info = search_results[0]
                            available = domain_info.get('Available', 'no').lower() == 'yes'
                            logger.info(f"Domain {domain} availability: {'Available' if available else 'Not Available'}")
                            return available
                        elif isinstance(search_results, dict) and 'Domain' in search_results:
                            # Handle object format: {'Domain': {'Available': 'true'}}
                            domain_info = search_results['Domain']
                            available = domain_info.get('Available', 'false').lower() == 'true'
                            logger.info(f"Domain {domain} availability: {'Available' if available else 'Not Available'}")
                            return available
                    elif 'Domain' in search_response:
                        # Alternative response structure
                        domain_info = search_response['Domain']
                        available = domain_info.get('Available', 'false').lower() == 'true'
                        logger.info(f"Domain {domain} availability: {'Available' if available else 'Not Available'}")
                        return available
                else:
                    # Check if domain is not available (response code != 0)
                    logger.info(f"Domain {domain} availability: Not Available (ResponseCode: {search_response.get('ResponseCode', 'unknown')})")
                    return False
            
            logger.warning(f"Could not parse availability response for {domain}")
            return False
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error checking availability for {domain}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error checking availability for {domain}: {e}")
            return False
    
    def register_domain(self, domain, years=1):
        """Register domain with Dynadot"""
        try:
            data = {
                'key': self.api_key,
                'command': 'register',
                'domain': domain,
                'duration': years
            }
            
            logger.info(f"Attempting to register {domain} via Dynadot API")
            response = self.session.get(self.api_url, params=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Dynadot registration response: {result}")
            
            # Parse Dynadot response
            if 'RegisterResponse' in result:
                register_response = result['RegisterResponse']
                if 'SuccessCode' in register_response:
                    success_code = register_response['SuccessCode']
                    if success_code == '0':
                        logger.info(f"SUCCESS: Domain {domain} registered successfully via Dynadot")
                        return True, f"Successfully registered {domain}"
                    else:
                        error_msg = register_response.get('Error', 'Unknown error')
                        logger.error(f"FAILED: Domain {domain} registration failed: {error_msg}")
                        return False, error_msg
                elif 'Status' in register_response:
                    status = register_response['Status']
                    if status.lower() == 'success':
                        logger.info(f"SUCCESS: Domain {domain} registered successfully via Dynadot")
                        return True, f"Successfully registered {domain}"
                    else:
                        error_msg = register_response.get('Error', 'Unknown error')
                        logger.error(f"FAILED: Domain {domain} registration failed: {error_msg}")
                        return False, error_msg
            
            logger.error(f"Could not parse registration response for {domain}")
            return False, "Could not parse registration response"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error registering {domain}: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error registering {domain}: {e}")
            return False, str(e)
    
    def test_api_connection(self):
        """Test API connection and credentials"""
        try:
            data = {
                'key': self.api_key,
                'command': 'account_info'
            }
            
            logger.info("Testing Dynadot API connection")
            response = self.session.get(self.api_url, params=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Dynadot API test response: {result}")
            
            if 'AccountInfoResponse' in result:
                logger.info("SUCCESS: Dynadot API credentials are valid")
                return True
            else:
                logger.error("FAILED: Invalid Dynadot API response")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error testing Dynadot API: {e}")
            return False
        except Exception as e:
            logger.error(f"Error testing Dynadot API: {e}")
            return False

if __name__ == "__main__":
    # Test Dynadot API
    api = DynadotAPI()
    
    if not DYNADOT_API_KEY:
        print("ERROR: DYNADOT_API_KEY not configured")
        print("Please set your Dynadot API key in config.py or environment variable")
        exit(1)
    
    print("Testing Dynadot API...")
    
    # Test connection
    if api.test_api_connection():
        print("API connection: SUCCESS")
        
        # Test domain availability
        test_domain = "test-domain-12345.com"
        available = api.check_domain_availability(test_domain)
        print(f"Domain availability check: {'Available' if available else 'Not Available'}")
        
        if available:
            # Test registration (commented out to avoid accidental registration)
            # success, message = api.register_domain(test_domain)
            # print(f"Registration test: {'Success' if success else 'Failed'} - {message}")
            print("Registration test: Skipped (uncomment to test)")
        
    else:
        print("API connection: FAILED")
        print("Please check your Dynadot API key and internet connection")
