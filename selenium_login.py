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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User credentials
username = 'test@example.com'
password = 'mypassword'

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
# options.add_argument("--incognito")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

try:
    # Initialize cookies variable
    cookies = []

    # Open the Microsoft SSO login page
    # replace the below with you SSO login URL
    driver.get("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=4765445b-32c6-49b0-83e6-1d93765276ca&redirect_uri=https%3A%2F%2Fwww.office.com%2Flandingv2&response_type=code%20id_token&scope=openid%20profile%20https%3A%2F%2Fwww.office.com%2Fv2%2FOfficeHome.All&response_mode=form_post&nonce=638545153408414506.MzE3ZTY3YjktYjgwZC00OGEwLTg4ZWMtZWIyMGE4MmM5ZWEzODFhMTkzMmQtOWI3My00OTVlLTg0ZWItN2VmN2EyOWJiNzA2&ui_locales=en-US&mkt=en-US&client-request-id=11777e48-7be8-4bcf-bdee-bc27607ea79c&state=ujzzvIz73cBqlN7ax75pYVU-OJPcGptRfxIzXaO3mBA1_2Y-HlIScvlQANAHoqDacK8rWgJnH0YvOZvOdvUod5lfJcHDUhki5nIUAxWE9Jm60go933jIQaf9fH71dHkIPX0qclMwF05oWOKkR2DT7oDstLxLdBA49FaUjflCUirnKuQYmc1F5PIdEjHT0WYXeALtKhxJr_kmBtvAZcCfCdu2KYHtF07L2YeggUXJjc7GppSvMw9YVr_3xWqvScctGJ0ZC3jIu-ADfzfPzjhkDA")

    # Wait for the page to load completely
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Open a new tab using the keyboard shortcut (Cmd + T on macOS)
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.COMMAND + 't')

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

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

    # Handle additional steps if needed (e.g., MFA, consent screen)
    time.sleep(10)  # Adjust the sleep time as needed

    # Verify login was successful by checking for a known element on the landing page
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "displayName")))

    # Extract cookies and save to a file
    cookies = driver.get_cookies()
    data = {'username': username, 'cookies': cookies}
    logger.info(f"Data to be written to JSON: {data}")
    with open('cookies.json', 'w') as f:
        json.dump(data, f)

    logger.info(f"Logged in as: {username}")
    logger.info(f"Cookies: {cookies}")

finally:
    # Close the browser
    driver.quit()

# Print the cookies (for demonstration purposes)
print(cookies)
