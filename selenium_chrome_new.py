import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
from multiprocessing import Pool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User credentials
username = 'stauffer.test@marshall.usc.edu'
password = ']Y1kBC]2GmfjCmPh'

# Number of total logins
total_logins = 500
# Test duration in minutes
test_duration_minutes = 20
# Number of processes to use
num_processes = 10
# Number of logins per process
logins_per_process = total_logins // num_processes

def login_simulation(process_id):
    options = webdriver.ChromeOptions()
    try:
        chromedriver_path = ChromeDriverManager().install()
        logger.info(f"ChromeDriver installed at: {chromedriver_path}")
        
        # Ensure the chromedriver is executable
        os.chmod(chromedriver_path, 0o755)

        driver = webdriver.Chrome(service=ChromeService(chromedriver_path), options=options)
    except WebDriverException as e:
        logger.error(f"Error initializing Chrome driver: {e}")
        return

    start_time = time.time()
    end_time = start_time + test_duration_minutes * 60

    login_id = 0
    while time.time() < end_time and login_id < logins_per_process:
        try:
            # Reuse the same browser window for each login attempt
            driver.get("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=4765445b-32c6-49b0-83e6-1d93765276ca&redirect_uri=https%3A%2F%2Fwww.office.com%2Flandingv2&response_type=code%20id_token&scope=openid%20profile%20https%3A%2F%2Fwww.office.com%2Fv2%2FOfficeHome.All&response_mode=form_post&nonce=638545153408414506.MzE3ZTY3YjktYjgwZC00OGEwLTg4ZWMtZWIyMGE4MmM5ZWEzODFhMTkzMmQtOWI3My00OTVlLTg0ZWItN2VmN2EyOWJiNzA2&ui_locales=en-US&mkt=en-US&client-request-id=11777e48-7be8-4bcf-bdee-bc27607ea79c&state=ujzzvIz73cBqlN7ax75pYVU-OJPcGptRfxIzXaO3mBA1_2Y-HlIScvlQANAHoqDacK8rWgJnH0YvOZvOdvUod5lfJcHDUhki5nIUAxWE9Jm60go933jIQaf9fH71dHkIPX0qclMwF05oWOKkR2DT7oDstLxLdBA49FaUjflCUirnKuQYmc1F5PIdEjHT0WYXeALtKhxJr_kmBtvAZcCfCdu2KYHtF07L2YeggUXJjc7GppSvMw9YVr_3xWqvScctGJ0ZC3jIu-ADfzfPzjhkDA")

            # Wait for the page to load completely
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Check if we need to pick an account
            try:
                pick_account = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-test-id='stauffer.test@marshall.usc.edu']/div")))
                pick_account.click()

                # Wait for the password input field to be present and enter the password
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "i0118")))
                password_field = driver.find_element(By.ID, "i0118")
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)
            except TimeoutException:
                # No account picker, proceed normally
                # Wait for the username input field to be present and enter the username
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "i0116")))
                username_field = driver.find_element(By.ID, "i0116")
                username_field.send_keys(username)
                username_field.send_keys(Keys.RETURN)

                # Wait for the password input field to be present and enter the password
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "i0118")))
                password_field = driver.find_element(By.ID, "i0118")
                password_field.send_keys(password)
                password_field.send_keys(Keys.RETURN)

            # Wait for the stay signed in button to be present and click "No"
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "idBtn_Back")))
            stay_signed_in_button = driver.find_element(By.ID, "idBtn_Back")
            stay_signed_in_button.click()

            # Verify login was successful by checking for a known element on the landing page
            try:
                WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "O365_MainLink_NavMenu")))
                logger.info(f"Login successful for process {process_id}, login {login_id}")
            except TimeoutException:
                logger.error(f"Login failed or took too long for process {process_id}, login {login_id}.")
                continue

            # Extract cookies and save to a file
            cookies = driver.get_cookies()
            data = {'username': username, 'cookies': cookies}
            with open(f'cookies/cookies_process_{process_id}_login_{login_id}.json', 'w') as f:
                json.dump(data, f)

            logger.info(f"Logged in as: {username}, Process: {process_id}, Login: {login_id}")
            # Log only the values of the cookies
            for cookie in cookies:
                logger.info(f"Cookie name: {cookie['name']} - Value: {cookie['value']}")

            # Log out to prepare for the next login
            driver.get("https://login.microsoftonline.com/logout.srf")
            time.sleep(5)  # Wait for logout to complete

            login_id += 1

        except Exception as e:
            logger.error(f"An error occurred in process {process_id}, login {login_id}: {e}")
            # If an error occurs, refresh the browser and continue
            driver.refresh()
            time.sleep(5)  # Allow some time before retrying

    # Close the browser after all logins
    driver.quit()

if __name__ == "__main__":
    os.makedirs('cookies', exist_ok=True)
    with Pool(num_processes) as pool:
        pool.map(login_simulation, range(num_processes))

    logger.info("All login simulations completed.")
