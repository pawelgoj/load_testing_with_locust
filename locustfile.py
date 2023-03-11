from locust import HttpUser, between, task
from faker import Faker


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    faker = Faker()
    used_emails: list[str] = []
    used_names: list[str] = []

    # def on_start(self):
    #     self.client.post("/login", {
    #         "username": "test_user",
    #         "password": ""
    #     })

    @task
    def get_book_titles(self):
        self.client.get("/api/v1/books?page=2&limit=3&fields=title")


    @task
    def get_author(self):
        self.client.get("{{url}}/api/v1/authors/1")

    @task
    def register_new_user_log_in_and_log_out(self):

        max_iter = 20
        for _ in range(max_iter):

            user_name = self.faker.user_name()
            email = self.faker.email()
            password = self.faker.password()

            if user_name not in self.used_names\
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

        self.client.post("/api/v1/auth/login", data=data)

    def on_stop(self):
        # TODO
        # conect to db and clear created data


