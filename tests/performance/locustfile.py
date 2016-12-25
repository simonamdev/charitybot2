from locust import HttpLocust, TaskSet, task


class ApiBehaviour(TaskSet):
    def on_start(self):
        pass

    @task(1)
    def index(self):
        self.client.get('/')


class ApiUser(HttpLocust):
    task_set = ApiBehaviour
    min_wait = 5000
    max_wait = 9000
