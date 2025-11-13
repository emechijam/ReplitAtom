# main.py
import threading
import time
import os
import sys

# Add the current directory to the path to import sync.py
# This is necessary because Replit might run from a different context
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the main loop function from sync.py
from sync import main as sync_main 

def run_synchronizer_loop():
    """Wrapper function to run sync.py's main loop."""
    print("Starting Football Synchronizer Loop in a new thread...")
    try:
        sync_main()
    except Exception as e:
        print(f"CRITICAL ERROR in synchronizer thread: {e}")

if __name__ == "__main__":
    # 1. Start the main sync logic in a background thread
    t = threading.Thread(target=run_synchronizer_loop, name="CoreSyncLoop")
    t.daemon = True # Allows the main program to exit if Replit decides to stop it
    t.start()
    
    # 2. Keep the main process (and Replit) alive with a simple infinite loop
    print("Main thread active to keep the Repl alive.")
    while True:
        # We don't need a web server; just a brief sleep is enough 
        # to signal that the script is intentionally running.
        time.sleep(60)
