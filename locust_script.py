import json
import logging
from locust import HttpUser, between, task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://yourwebsite.com"

    def on_start(self):
        # Load cookies and username from file
        with open('cookies.json', 'r') as f:
            data = json.load(f)
        
        # logger.info(f"Data type: {type(data)}")
        # logger.info(f"Data content: {data}")

        # Ensure data is a dictionary
        if isinstance(data, dict):
            username = data['username']
            cookies = data['cookies']

            self.client.cookies.clear()
            for cookie in cookies:
                self.client.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', ''), path=cookie.get('path', '/'))
            
            # Log the username
            logger.info(f"Loaded cookies for user {username}")

    @task
    def index(self):
        self.client.get("/")

# Run Locust with: locust -f locust_script.py
