from locust import HttpLocust, TaskSet, task

event_name = 'performance'
api_path = '/api/v1/'
overlay_path = '/overlay/' + event_name
stats_path = '/stats/' + event_name


class ApiBehaviour(TaskSet):
    def on_start(self):
        pass

    @task(1)
    def index(self):
        self.client.get(api_path)

    @task(5)
    def overlay(self):
        self.client.get(overlay_path)

    @task(3)
    def stats(self):
        self.client.get(stats_path)


class ApiUser(HttpLocust):
    task_set = ApiBehaviour
    min_wait = 5000
    max_wait = 9000
