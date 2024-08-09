import subprocess
import time
import logging
from multiprocessing import Process

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_selenium_script():
    logger.info("Starting Selenium script to log in...")
    result = subprocess.run(["python3", "selenium_chrome_new.py"])
    logger.info("Selenium script completed with return code: %s", result.returncode)
    return result.returncode

def run_locust_script():
    # Wait for Selenium script to generate cookies.json
    time.sleep(5)  # Adjust the sleep time if necessary
    logger.info("Starting Locust...")
    locust_process = subprocess.Popen(["locust", "-f", "locust_script.py"])
    logger.info("Locust started.")
    locust_process.wait()
    logger.info("Locust process finished.")

def open_locust_web_interface():
    # Wait a few seconds to ensure Locust is started
    time.sleep(10)
    # Command to open Chrome
    chrome_command = [
        "open", "-na", "Google Chrome", "--args", "http://localhost:8089"
    ]
    # Open the Locust web interface in Chrome
    subprocess.run(chrome_command)
    logger.info("Locust web interface opened in Chrome.")

def main():
    selenium_process = Process(target=run_selenium_script)
    locust_process = Process(target=run_locust_script)
    web_interface_process = Process(target=open_locust_web_interface)

    # Start the Selenium and Locust processes
    selenium_process.start()
    locust_process.start()

    # Wait for Selenium process to complete
    selenium_process.join()

    if selenium_process.exitcode != 0:
        logger.error("Selenium script failed.")
        return

    # Start the web interface process
    web_interface_process.start()

    # Wait for Locust and web interface processes to complete
    locust_process.join()
    web_interface_process.join()

if __name__ == "__main__":
    main()
