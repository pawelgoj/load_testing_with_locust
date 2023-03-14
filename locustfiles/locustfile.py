import logging

from locust import HttpUser, between, task, tag, FastHttpUser
from faker import Faker
from dotenv import load_dotenv
import os
from types import ModuleType


load_dotenv()

# In config file on_test_start  and on_test_stop function
# Functions are run automatically by locust when imported
from common import config

class WebsiteUser(FastHttpUser):
    wait_time = between(2, 10)

    faker: ModuleType = Faker()
    
    used_emails: list[str] = []
    used_names: list[str] = [] 
    database_name: str = "book_library"
    host_db: str = "localhost"
    user_db: str = os.environ.get("USER")
    password_db: str = os.environ.get("PASSWORD")
    # run script in root directory.
    dump_file: str = "data_base_backup/database_dump.sql"

    def on_start(self):
        logging.info("New user starting task")

    @tag('book_titles')
    @task(3)
    def get_book_titles(self):
        for i in range(1, 3):
            # Validate response
            with self.client.get("/api/v1/books?page=%i&limit=3&fields=title" % i,
                                 catch_response=True) as response:

                if response.status_code == 200 \
                        and "data" in response.json().keys():

                    response.success()

    @tag('author')
    @task(3)
    def get_author(self):
        # grouping of requests
        for i in range(1, 6):
            self.client.get("/api/v1/authors/%i" % i, name="/api/v1/authors/[id]")

    @tag('register')
    @task(1)
    def register_new_user_and_log_in(self):

        max_iter = 20
        for _ in range(max_iter):

            user_name = self.faker.user_name()
            email = self.faker.email()
            password = self.faker.password()

            if user_name not in self.used_names \
                    and email not in self.used_emails:
                self.used_names.append(user_name)
                self.used_emails.append(email)

                break

        data = {
            "username": user_name,
            "password": password,
            "email": email
        }

        self.client.post("/api/v1/auth/register", json=data)

        data = {
            "username": user_name,
            "password": password,
        }

        self.client.post("/api/v1/auth/login", json=data)

    def on_stop(self):
        logging.info("User stop task")

