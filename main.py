# main.py - Final version for Replit 24/7 Free Hosting
import threading
import time
import os
import sys
from flask import Flask
import logging
from datetime import datetime

# --- Configuration ---
# Set the desired log format before importing any modules that use logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MAIN] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Add the current directory to the path to allow direct import of sync.py and predictor.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the core loop function from sync.py
try:
    from sync import main as sync_main 
except ImportError as e:
    logging.error(f"Failed to import sync.py: {e}. Check file path and naming.")
    sys.exit(1)


# --- Flask Server Setup (The Keep-Alive) ---
app = Flask(__name__)
last_sync_time = "Never"
last_sync_success = False

@app.route('/')
def home():
    """Provides a basic status message for the Uptime Monitor."""
    status = "SUCCESS" if last_sync_success else "RUNNING/ERROR"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Football Sync Status</title></head>
    <body>
        <h1>Football Synchronizer Status</h1>
        <p><strong>Status:</strong> {status} (Last core loop attempt completed: {last_sync_time})</p>
        <p>This endpoint is primarily for external Uptime Monitoring to prevent the Repl from sleeping.</p>
    </body>
    </html>
    """
    return html_content

def run_flask_server():
    """Runs the Flask server in a blocking manner."""
    logging.info("Starting Flask Keep-Alive Server on port 8080...")
    # Replit automatically exposes port 8080 (or any open port)
    app.run(host='0.0.0.0', port=8080)


# --- Core Synchronizer Logic ---
def run_synchronizer_loop():
    """Wrapper function to execute sync.py's main loop and update status."""
    global last_sync_time, last_sync_success
    
    logging.info("Starting Core Synchronizer Loop in background thread...")
    
    # We rely on the internal loop (while True) within sync.py's main()
    try:
        sync_main()
        # This line is theoretically unreachable because sync.main() runs an infinite loop
    except Exception as e:
        # If the loop breaks due to a critical error (e.g., DB crash)
        logging.critical(f"CRITICAL: Core synchronizer loop terminated with error: {e}")
        last_sync_success = False
    finally:
        last_sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")


if __name__ == "__main__":
    # 1. Start the core sync loop (the infinite job) in a background thread
    t_sync = threading.Thread(target=run_synchronizer_loop, name="CoreSyncWorker")
    t_sync.daemon = True 
    t_sync.start()
    
    # 2. Start the Flask server (the keep-alive mechanism) in the main thread
    # This must run on the main thread to be auto-discovered by Replit's web view
    run_flask_server()
