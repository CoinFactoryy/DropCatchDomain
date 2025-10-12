import schedule
import time
import threading
import logging
from datetime import datetime, timedelta
from check_status import DomainStatusChecker
from catcher import DomainCatcher
from notify import NotificationManager
from config import (
    CHECK_INTERVAL, REGISTRAR_DROP_TIMES, DROP_BUFFER_TIME,
    LOG_LEVEL, LOG_FILE
)

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

class DropScheduler:
    def __init__(self):
        self.checker = DomainStatusChecker()
        self.catcher = DomainCatcher()
        self.notifier = NotificationManager()
        self.scheduled_domains = {}  # Track scheduled domains
        self.running = False
        
    def calculate_drop_time(self, domain_info):
        """Calculate approximate drop time based on status and registrar"""
        # PendingDelete domains typically drop 5 days after expiry
        # This is an approximation - actual times vary by registrar
        base_drop_time = datetime.now() + timedelta(days=5)
        
        # Adjust based on registrar
        registrar = domain_info.get('registrar', '').lower()
        
        # Look up registrar-specific drop time
        drop_time_config = REGISTRAR_DROP_TIMES.get('default')
        for reg_name, config in REGISTRAR_DROP_TIMES.items():
            if reg_name != 'default' and reg_name in registrar:
                drop_time_config = config
                break
        
        # Set the drop time
        drop_time = base_drop_time.replace(
            hour=drop_time_config['hour'],
            minute=drop_time_config['minute'],
            second=0,
            microsecond=0
        )
        
        # Add buffer time before actual drop
        drop_time -= timedelta(seconds=DROP_BUFFER_TIME)
        
        logger.info(f"Calculated drop time for {domain_info['domain']}: {drop_time}")
        return drop_time
    
    def schedule_domain_catch(self, domain_info):
        """Schedule a domain catch attempt"""
        domain = domain_info['domain']
        
        # Check if already scheduled
        if domain in self.scheduled_domains:
            logger.info(f"Domain {domain} already scheduled, skipping")
            return
        
        drop_time = self.calculate_drop_time(domain_info)
        
        # Don't schedule if drop time is in the past
        if drop_time <= datetime.now():
            logger.warning(f"Drop time for {domain} is in the past, scheduling immediately")
            drop_time = datetime.now() + timedelta(minutes=1)
        
        logger.info(f"Scheduling catch for {domain} at {drop_time}")
        
        # Schedule the catch attempt
        schedule.every().day.at(drop_time.strftime("%H:%M")).do(
            self.attempt_catch, domain_info
        )
        
        # Track scheduled domain
        self.scheduled_domains[domain] = {
            'domain_info': domain_info,
            'scheduled_time': drop_time,
            'status': 'scheduled'
        }
        
        # Notify about scheduled catch
        self.notifier.send_scheduled_notification(domain, drop_time)
        
        logger.info(f"✅ Domain {domain} scheduled for catch at {drop_time}")
    
    def attempt_catch(self, domain_info):
        """Attempt to catch a domain"""
        domain = domain_info['domain']
        logger.info(f"🚀 Starting catch attempt for {domain}...")
        
        # Update status
        if domain in self.scheduled_domains:
            self.scheduled_domains[domain]['status'] = 'attempting'
        
        try:
            success = self.catcher.catch_domain(domain)
            stats = self.catcher.get_catch_stats(domain)
            
            if success:
                # Update status
                if domain in self.scheduled_domains:
                    self.scheduled_domains[domain]['status'] = 'success'
                
                # Send success notification
                details = f"Attempts: {stats['attempts']}\nMessage: {stats['message']}"
                self.notifier.send_success_notification(domain, details)
                
                logger.info(f"🎉 Successfully caught {domain}!")
            else:
                # Update status
                if domain in self.scheduled_domains:
                    self.scheduled_domains[domain]['status'] = 'failed'
                
                # Send failure notification
                reason = f"Failed after {stats['attempts']} attempts: {stats['message']}"
                self.notifier.send_failure_notification(domain, reason)
                
                logger.warning(f"❌ Failed to catch {domain}")
                
        except Exception as e:
            logger.error(f"Error during catch attempt for {domain}: {e}")
            
            # Update status
            if domain in self.scheduled_domains:
                self.scheduled_domains[domain]['status'] = 'error'
            
            # Send error notification
            self.notifier.send_failure_notification(domain, f"Error: {str(e)}")
    
    def check_pending_domains(self):
        """Check for new pendingDelete domains"""
        logger.info("Checking for pendingDelete domains...")
        
        try:
            pending_domains = self.checker.monitor_all_domains()
            
            for domain_info in pending_domains:
                domain = domain_info['domain']
                
                # Check if already scheduled
                if domain in self.scheduled_domains:
                    logger.info(f"Domain {domain} already scheduled, skipping")
                    continue
                
                # Schedule catch attempt
                self.schedule_domain_catch(domain_info)
                
                # Send monitoring notification
                self.notifier.send_monitoring_notification(
                    domain, domain_info['status'], domain_info['registrar']
                )
            
            if not pending_domains:
                logger.info("No new pendingDelete domains found")
                
        except Exception as e:
            logger.error(f"Error checking pending domains: {e}")
    
    def get_scheduled_domains(self):
        """Get list of scheduled domains"""
        return self.scheduled_domains.copy()
    
    def cancel_domain(self, domain):
        """Cancel a scheduled domain catch"""
        if domain in self.scheduled_domains:
            # Note: schedule library doesn't have a direct way to cancel specific jobs
            # This is a limitation - in production, you'd want a more sophisticated scheduler
            logger.info(f"Cancelling scheduled catch for {domain}")
            self.scheduled_domains[domain]['status'] = 'cancelled'
            return True
        return False
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        logger.info("Starting domain monitoring system...")
        self.running = True
        
        # Check for pendingDelete domains every hour
        schedule.every().hour.do(self.check_pending_domains)
        
        # Run initial check
        logger.info("Running initial domain check...")
        self.check_pending_domains()
        
        # Keep the scheduler running
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Monitoring interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Continue after error
        
        self.cleanup()
    
    def stop_monitoring(self):
        """Stop the monitoring loop"""
        logger.info("Stopping domain monitoring...")
        self.running = False
    
    def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up resources...")
        self.catcher.cleanup()
        
        # Print final summary
        if self.scheduled_domains:
            logger.info("Scheduled domains summary:")
            for domain, info in self.scheduled_domains.items():
                status = info['status']
                scheduled_time = info['scheduled_time']
                logger.info(f"  {domain}: {status} (scheduled: {scheduled_time})")
        else:
            logger.info("No domains were scheduled")

def main():
    """Main function to run the scheduler"""
    scheduler = DropScheduler()
    
    try:
        scheduler.start_monitoring()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        scheduler.stop_monitoring()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        scheduler.stop_monitoring()

if __name__ == "__main__":
    main()
