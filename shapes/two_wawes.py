from locust import LoadTestShape

class TripleRamp(LoadTestShape):

    min_users = 2
    peak_one_users = 4
    peak_two_users = 8
    peak_three_users = 10
    time_limit = 60

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit / 5:
            user_count = min_users
        elif run_time < 2 * (self.time_limit / 5):
            user_count = peak_one_users
        elif run_time < 3 * (self.time_limit / 5):
            user_count = peak_two_users
        elif run_time < 4 * (self.time_limit / 5):
            user_count = peak_three_users
        else:
            user_count = min_users

        spawn_rate = users_count
        return (round(user_count), round(spawn_rate))

