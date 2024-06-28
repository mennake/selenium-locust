import json
import logging
from locust import HttpUser, between, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a global counter for the number of logins
login_counter = 0

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://bid-uat.marshall.usc.edu"

    def on_start(self):
        global login_counter

        # Load cookies and username from file
        with open('cookies.json', 'r') as f:
            data = json.load(f)
        
        # logger.info(f"Data type: {type(data)}")
        # logger.info(f"Data content: {data}")

        if isinstance(data, dict):
            username = data['username']
            cookies = data['cookies']

            self.client.cookies.clear()
            for cookie in cookies:
                self.client.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', ''), path=cookie.get('path', '/'))

             # Increment the login counter
            login_counter += 1
            
            # Log the username and login count for testing
            logger.info(f"Loaded cookies for user {username}. This is login number {login_counter}. Logging into {self.host}")

    @task
    def index(self):
        self.client.get("/")
