import sqlite3
import logging
from datetime import datetime
from config import DATABASE_FILE, LOG_LEVEL, LOG_FILE

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

class DomainDatabase:
    def __init__(self):
        self.db_file = DATABASE_FILE
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Create domains table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS domains (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain TEXT UNIQUE NOT NULL,
                        status TEXT NOT NULL,
                        registrar TEXT,
                        expiry_date TEXT,
                        last_checked DATETIME,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create catch_attempts table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS catch_attempts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain TEXT NOT NULL,
                        scheduled_time DATETIME,
                        attempted_time DATETIME,
                        success BOOLEAN,
                        attempts INTEGER,
                        message TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create notifications table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        domain TEXT NOT NULL,
                        notification_type TEXT NOT NULL,
                        message TEXT,
                        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        success BOOLEAN
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def add_domain(self, domain, status='unknown', registrar='unknown', expiry_date=''):
        """Add or update a domain in the database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Check if domain exists
                cursor.execute('SELECT id FROM domains WHERE domain = ?', (domain,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing domain
                    cursor.execute('''
                        UPDATE domains 
                        SET status = ?, registrar = ?, expiry_date = ?, 
                            last_checked = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                        WHERE domain = ?
                    ''', (status, registrar, expiry_date, domain))
                    logger.info(f"Updated domain {domain} in database")
                else:
                    # Insert new domain
                    cursor.execute('''
                        INSERT INTO domains (domain, status, registrar, expiry_date, last_checked)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ''', (domain, status, registrar, expiry_date))
                    logger.info(f"Added domain {domain} to database")
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding domain {domain}: {e}")
            return False
    
    def get_domain(self, domain):
        """Get domain information from database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT domain, status, registrar, expiry_date, last_checked, created_at, updated_at
                    FROM domains WHERE domain = ?
                ''', (domain,))
                
                result = cursor.fetchone()
                if result:
                    return {
                        'domain': result[0],
                        'status': result[1],
                        'registrar': result[2],
                        'expiry_date': result[3],
                        'last_checked': result[4],
                        'created_at': result[5],
                        'updated_at': result[6]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting domain {domain}: {e}")
            return None
    
    def get_all_domains(self):
        """Get all domains from database"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT domain, status, registrar, expiry_date, last_checked, created_at, updated_at
                    FROM domains ORDER BY updated_at DESC
                ''')
                
                results = cursor.fetchall()
                domains = []
                for result in results:
                    domains.append({
                        'domain': result[0],
                        'status': result[1],
                        'registrar': result[2],
                        'expiry_date': result[3],
                        'last_checked': result[4],
                        'created_at': result[5],
                        'updated_at': result[6]
                    })
                
                return domains
                
        except Exception as e:
            logger.error(f"Error getting all domains: {e}")
            return []
    
    def get_pending_delete_domains(self):
        """Get all domains with pendingDelete status"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT domain, status, registrar, expiry_date, last_checked, created_at, updated_at
                    FROM domains WHERE status = 'pendingDelete' ORDER BY updated_at DESC
                ''')
                
                results = cursor.fetchall()
                domains = []
                for result in results:
                    domains.append({
                        'domain': result[0],
                        'status': result[1],
                        'registrar': result[2],
                        'expiry_date': result[3],
                        'last_checked': result[4],
                        'created_at': result[5],
                        'updated_at': result[6]
                    })
                
                return domains
                
        except Exception as e:
            logger.error(f"Error getting pendingDelete domains: {e}")
            return []
    
    def add_catch_attempt(self, domain, scheduled_time=None, attempted_time=None, success=False, attempts=0, message=''):
        """Add a catch attempt record"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO catch_attempts (domain, scheduled_time, attempted_time, success, attempts, message)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (domain, scheduled_time, attempted_time, success, attempts, message))
                
                conn.commit()
                logger.info(f"Added catch attempt for {domain} to database")
                return True
                
        except Exception as e:
            logger.error(f"Error adding catch attempt for {domain}: {e}")
            return False
    
    def get_catch_attempts(self, domain=None):
        """Get catch attempts (optionally filtered by domain)"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                if domain:
                    cursor.execute('''
                        SELECT domain, scheduled_time, attempted_time, success, attempts, message, created_at
                        FROM catch_attempts WHERE domain = ? ORDER BY created_at DESC
                    ''', (domain,))
                else:
                    cursor.execute('''
                        SELECT domain, scheduled_time, attempted_time, success, attempts, message, created_at
                        FROM catch_attempts ORDER BY created_at DESC
                    ''')
                
                results = cursor.fetchall()
                attempts = []
                for result in results:
                    attempts.append({
                        'domain': result[0],
                        'scheduled_time': result[1],
                        'attempted_time': result[2],
                        'success': result[3],
                        'attempts': result[4],
                        'message': result[5],
                        'created_at': result[6]
                    })
                
                return attempts
                
        except Exception as e:
            logger.error(f"Error getting catch attempts: {e}")
            return []
    
    def add_notification(self, domain, notification_type, message, success=True):
        """Add a notification record"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO notifications (domain, notification_type, message, success)
                    VALUES (?, ?, ?, ?)
                ''', (domain, notification_type, message, success))
                
                conn.commit()
                logger.info(f"Added notification for {domain} to database")
                return True
                
        except Exception as e:
            logger.error(f"Error adding notification for {domain}: {e}")
            return False
    
    def get_notifications(self, domain=None, limit=50):
        """Get notifications (optionally filtered by domain)"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                if domain:
                    cursor.execute('''
                        SELECT domain, notification_type, message, sent_at, success
                        FROM notifications WHERE domain = ? ORDER BY sent_at DESC LIMIT ?
                    ''', (domain, limit))
                else:
                    cursor.execute('''
                        SELECT domain, notification_type, message, sent_at, success
                        FROM notifications ORDER BY sent_at DESC LIMIT ?
                    ''', (limit,))
                
                results = cursor.fetchall()
                notifications = []
                for result in results:
                    notifications.append({
                        'domain': result[0],
                        'notification_type': result[1],
                        'message': result[2],
                        'sent_at': result[3],
                        'success': result[4]
                    })
                
                return notifications
                
        except Exception as e:
            logger.error(f"Error getting notifications: {e}")
            return []
    
    def cleanup_old_records(self, days=30):
        """Clean up old records to keep database size manageable"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Clean up old notifications
                cursor.execute('''
                    DELETE FROM notifications 
                    WHERE sent_at < datetime('now', '-{} days')
                '''.format(days))
                
                # Clean up old catch attempts
                cursor.execute('''
                    DELETE FROM catch_attempts 
                    WHERE created_at < datetime('now', '-{} days')
                '''.format(days))
                
                conn.commit()
                logger.info(f"Cleaned up records older than {days} days")
                return True
                
        except Exception as e:
            logger.error(f"Error cleaning up old records: {e}")
            return False
    
    def get_stats(self):
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Count domains by status
                cursor.execute('SELECT status, COUNT(*) FROM domains GROUP BY status')
                status_counts = dict(cursor.fetchall())
                
                # Count catch attempts
                cursor.execute('SELECT COUNT(*) FROM catch_attempts')
                total_attempts = cursor.fetchone()[0]
                
                # Count successful catches
                cursor.execute('SELECT COUNT(*) FROM catch_attempts WHERE success = 1')
                successful_catches = cursor.fetchone()[0]
                
                # Count notifications
                cursor.execute('SELECT COUNT(*) FROM notifications')
                total_notifications = cursor.fetchone()[0]
                
                return {
                    'status_counts': status_counts,
                    'total_attempts': total_attempts,
                    'successful_catches': successful_catches,
                    'total_notifications': total_notifications
                }
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}

if __name__ == "__main__":
    db = DomainDatabase()
    
    # Test database operations
    print("Testing database operations...")
    
    # Add a test domain
    db.add_domain('test.com', 'pendingDelete', 'Test Registrar', '2024-12-31')
    
    # Get the domain
    domain_info = db.get_domain('test.com')
    print(f"Domain info: {domain_info}")
    
    # Add a catch attempt
    db.add_catch_attempt('test.com', success=True, attempts=100, message='Test catch')
    
    # Add a notification
    db.add_notification('test.com', 'success', 'Test notification')
    
    # Get stats
    stats = db.get_stats()
    print(f"Database stats: {stats}")
    
    print("Database test completed!")
