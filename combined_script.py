import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Run the Selenium script to log in and save cookies
logger.info("Starting Selenium script to log in...")
subprocess.run(["python3", "selenium_login.py"])
logger.info("Selenium script completed.")

# Step 2: Start Locust
logger.info("Starting Locust...")
locust_process = subprocess.Popen(["locust", "-f", "locust_script.py"])

# Step 3: Open the Locust web interface in Chrome
# Wait a few seconds to ensure Locust is started
time.sleep(5)

# Command to open Chrome
chrome_command = [
    "open", "-na", "Google Chrome", "--args", "http://localhost:8089"
]

# Open the Locust web interface in Chrome
subprocess.run(chrome_command)

# Wait for Locust to finish
locust_process.wait()
