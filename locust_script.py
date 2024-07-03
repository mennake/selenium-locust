import json
import logging
import random
import os
from locust import HttpUser, between, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a global counter for the number of logins
login_counter = 0

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://bid-uat.marshall.usc.edu"

    # on_start method is called for each simulated user
    def on_start(self):
        global login_counter

        # List all cookie files in the cookies directory
        cookie_files = [f for f in os.listdir('cookies') if f.startswith('cookies_') and f.endswith('.json')]

        # Randomly select one of the cookie files
        selected_file = random.choice(cookie_files)

        # Load cookies and username from the selected file
        with open(os.path.join('cookies', selected_file), 'r') as f:
            data = json.load(f)

        if isinstance(data, dict):
            username = data['username']
            cookies = data['cookies']

            self.client.cookies.clear()
            for cookie in cookies:
                self.client.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', ''), path=cookie.get('path', '/'))

            # Log each cookie name and value
            for cookie in cookies:
                logger.info(f"Cookie name: {cookie['name']} - Value: {cookie['value']}")

            # Increment the login counter to validate multiple logins
            login_counter += 1
            
            # Log the username and login count for testing
            logger.info(f"Loaded cookies for user {username} from {selected_file}. This is login number {login_counter}. Logging into {self.host}")

    @task
    def index(self):
        self.client.get("/")
