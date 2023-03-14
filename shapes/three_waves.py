from locust import LoadTestShape

class TripleRamp(LoadTestShape):

    min_users = 5
    peak_one_users = 10
    peak_two_users = 20
    peak_three_users = 30
    time_limit = 120

    def tick(self):
        run_time = round(self.get_run_time())

        users_count = 1

        if run_time < self.time_limit / 5:
            user_count = self.min_users
        elif run_time < 2 * (self.time_limit / 5):
            user_count = self.peak_one_users
        elif run_time < 3 * (self.time_limit / 5):
            user_count = self.peak_two_users
        elif run_time < 4 * (self.time_limit / 5):
            user_count = self.peak_three_users
        else:
            user_count = self.min_users

        spawn_rate = users_count
        return (round(user_count), round(spawn_rate))

