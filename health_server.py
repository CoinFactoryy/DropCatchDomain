#!/usr/bin/env python3
"""
Simple health check server for Railway deployment
"""
import os
import threading
import time
from flask import Flask, jsonify
from scheduler import DropScheduler

# Create Flask app
app = Flask(__name__)

# Global scheduler instance
scheduler = None

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'domain-monitor',
        'timestamp': time.time()
    }), 200

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        'service': 'Domain Monitor',
        'status': 'running',
        'endpoints': ['/health']
    }), 200

def start_scheduler():
    """Start the domain scheduler in a separate thread"""
    global scheduler
    try:
        scheduler = DropScheduler()
        scheduler.start_monitoring()
    except Exception as e:
        print(f"Scheduler error: {e}")

if __name__ == '__main__':
    # Start scheduler in background thread
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Start Flask server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
