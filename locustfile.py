from locust import HttpUser, between, task, tag
import common.auth
from faker import Faker
from dotenv import load_dotenv
import os
import subprocess
from types import ModuleType
import mysql.connector

load_dotenv()


class WebsiteUser(HttpUser):
    wait_time = between(2, 10)
    faker: ModuleType = Faker()
    used_emails: list[str] = []
    used_names: list[str] = []
    database_name: str = "book_library"
    host_db: str = "localhost"
    user_db: str = os.environ.get("USER")
    password_db: str = os.environ.get("PASSWORD")
    dump_file: str = "database_dump.sql"

    def on_start(self):
        # dump test database state before tests
        process = subprocess.Popen(["mysqldump", f"--user={self.user_db}", f"--password={self.password_db}",
                                    f"--host={self.host_db}", f"{self.database_name}", "--result-file=database_dump.sql"])
        process.wait()

    @tag('book_titles')
    @task(3)
    def get_book_titles(self):
        for i in range(1, 3):
            self.client.get("/api/v1/books?page=%i&limit=3&fields=title" % i)

    @tag('author')
    @task(3)
    def get_author(self):
        for i in range(1, 6):
            self.client.get("/api/v1/authors/%i" % i)

    @tag('register')
    @task(1)
    def register_new_user_log_in_and_log_out(self):

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
        """
        Restore the state of the database given from before load testing
        auth_plugin must be mysql_native_password ,in mySQL 8.0
        caching_sha2_password is the default authentication plugin rather than
        """

        mydb = mysql.connector.connect(
            buffered=True,
            host=self.host_db,
            user=self.user_db,
            password=self.password_db
        )

        mycursor = mydb.cursor()
        mycursor.execute(f"drop database {self.database_name}")
        mydb.commit()

        mycursor.execute(f"create database {self.database_name}")
        mydb.commit()
        mydb.close()

        subprocess.run(f"mysql --user={self.user_db} --password={self.password_db} --host={self.host_db} {self.database_name}"
                  + f" < {self.dump_file}", shell=True)

