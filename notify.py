import requests
import json
import logging
from datetime import datetime
from config import (
    DISCORD_WEBHOOK, EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD,
    LOG_LEVEL, LOG_FILE
)
from database import DomainDatabase

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

class NotificationManager:
    def __init__(self):
        self.discord_webhook = DISCORD_WEBHOOK
        self.email_username = EMAIL_USERNAME
        self.email_password = EMAIL_PASSWORD
        self.smtp_server = EMAIL_SMTP_SERVER
        self.smtp_port = EMAIL_SMTP_PORT
        self.db = DomainDatabase()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DomainCatcher/1.0'
        })
    
    def send_email(self, subject, body, to_email=None):
        """Send email notification (optional for beginners)"""
        if not self.email_username or not self.email_password:
            logger.debug("Email credentials not configured - skipping email notification")
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            if not to_email:
                to_email = self.email_username
            
            msg = MIMEMultipart()
            msg['From'] = self.email_username
            msg['To'] = to_email
            msg['Subject'] = f"[DomainCatcher] {subject}"
            
            # Add timestamp to body
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            full_body = f"{body}\n\nTimestamp: {timestamp}"
            
            msg.attach(MIMEText(full_body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            
            text = msg.as_string()
            server.sendmail(self.email_username, to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully: {subject}")
            return True
            
        except ImportError:
            logger.warning("Email libraries not available - install with: pip install email")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False
    
    def send_discord(self, message, title=None, color=0x00ff00):
        """Send Discord notification via webhook (primary method for beginners)"""
        if not self.discord_webhook:
            logger.warning("Discord webhook not configured - this is the primary notification method")
            return False
        
        try:
            # Add timestamp to message
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            
            data = {
                "content": message,
                "username": "Domain Catcher",
                "avatar_url": "https://cdn-icons-png.flaticon.com/512/3176/3176363.png"
            }
            
            if title:
                data["embeds"] = [{
                    "title": title,
                    "description": message,
                    "color": color,
                    "timestamp": datetime.now().isoformat(),
                    "footer": {
                        "text": "DomainCatcher Beginner Combo"
                    }
                }]
            
            response = self.session.post(self.discord_webhook, json=data, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Discord notification sent successfully: {title or message}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Discord webhook request failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending Discord notification: {e}")
            return False
    
    def send_success_notification(self, domain, details=None):
        """Send success notification for caught domain"""
        subject = f"✅ Successfully caught {domain}!"
        message = f"Domain {domain} has been registered successfully."
        
        if details:
            message += f"\n\nDetails:\n{details}"
        
        # Send Discord with green color (primary method)
        discord_sent = self.send_discord(message, subject, color=0x00ff00)
        
        # Send email (optional)
        email_sent = self.send_email(subject, message)
        
        # Log to database
        self.db.add_notification(domain, 'success', message, discord_sent or email_sent)
        
        return discord_sent or email_sent
    
    def send_failure_notification(self, domain, reason=None):
        """Send failure notification for missed domain"""
        subject = f"❌ Failed to catch {domain}"
        message = f"Domain {domain} was not available for registration."
        
        if reason:
            message += f"\n\nReason: {reason}"
        
        # Send Discord with red color (primary method)
        discord_sent = self.send_discord(message, subject, color=0xff0000)
        
        # Send email (optional)
        email_sent = self.send_email(subject, message)
        
        # Log to database
        self.db.add_notification(domain, 'failure', message, discord_sent or email_sent)
        
        return discord_sent or email_sent
    
    def send_monitoring_notification(self, domain, status, registrar=None):
        """Send notification about domain status change"""
        subject = f"🔍 Domain Status Update: {domain}"
        message = f"Domain {domain} status: {status}"
        
        if registrar:
            message += f"\nRegistrar: {registrar}"
        
        # Send Discord with blue color (primary method)
        discord_sent = self.send_discord(message, subject, color=0x0099ff)
        
        # Send email (optional)
        email_sent = self.send_email(subject, message)
        
        # Log to database
        self.db.add_notification(domain, 'monitoring', message, discord_sent or email_sent)
        
        return discord_sent or email_sent
    
    def send_scheduled_notification(self, domain, drop_time):
        """Send notification about scheduled catch attempt"""
        subject = f"⏰ Domain Catch Scheduled: {domain}"
        message = f"Domain {domain} scheduled for catch at {drop_time}"
        
        # Send Discord with orange color (primary method)
        discord_sent = self.send_discord(message, subject, color=0xff9900)
        
        # Send email (optional)
        email_sent = self.send_email(subject, message)
        
        # Log to database
        self.db.add_notification(domain, 'scheduled', message, discord_sent or email_sent)
        
        return discord_sent or email_sent
    
    def send_notification(self, subject, body, notification_type="info"):
        """Send general notification via all configured channels"""
        logger.info(f"Notification: {subject}")
        logger.info(f"Body: {body}")
        
        # Determine color based on notification type
        color_map = {
            "success": 0x00ff00,
            "error": 0xff0000,
            "warning": 0xff9900,
            "info": 0x0099ff
        }
        color = color_map.get(notification_type, 0x0099ff)
        
        # Send Discord (primary method)
        discord_sent = self.send_discord(body, subject, color=color)
        
        # Send email (optional)
        email_sent = self.send_email(subject, body)
        
        return discord_sent or email_sent
    
    def test_notifications(self):
        """Test all notification channels"""
        logger.info("Testing notification channels...")
        
        test_subject = "Test Notification - Beginner Combo"
        test_body = "This is a test message from the DomainCatcher Beginner Combo system."
        
        # Test Discord (primary method)
        discord_result = self.send_discord(test_body, test_subject)
        logger.info(f"Discord test: {'SUCCESS' if discord_result else 'FAILED'}")
        
        # Test email (optional)
        email_result = self.send_email(test_subject, test_body)
        logger.info(f"Email test: {'SUCCESS' if email_result else 'FAILED'}")
        
        return discord_result or email_result

if __name__ == "__main__":
    notifier = NotificationManager()
    
    # Test notifications
    print("Testing notification system...")
    success = notifier.test_notifications()
    
    if success:
        print("SUCCESS: Notification system test completed")
    else:
        print("FAILED: Notification system test failed")
        print("Please check your configuration and try again")
