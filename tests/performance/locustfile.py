from locust import HttpLocust, TaskSet, task

event_name = 'performance'
api_path = '/api/v1/'
overlay_path = '/overlay/' + event_name
stats_path = '/stats/' + event_name
static_path = '/static/'

static_files = [
    'js/ui.js',
    'js/stats_console.js',
    'css/spinner.css',
    'css/main.css'
]

stats_api_calls = [
    'event/' + event_name + '/donations/distribution',
    'event/' + event_name + '/donations',
    'event/' + event_name + '/donations/info'
]


class OverlayBehaviour(TaskSet):
    @task
    def overlay(self):
        self.client.get(overlay_path)


class UserBehaviour(TaskSet):
    @task
    def stats(self):
        self.client.get(stats_path)
        for file in static_files:
            self.client.get(static_path + file)
        for call in stats_api_calls:
            self.client.get(api_path + call)


class StatsConsoleCalls(HttpLocust):
    task_set = UserBehaviour
    min_wait = 5000
    max_wait = 30000


class OverlayCalls(HttpLocust):
    task_set = OverlayBehaviour
    min_wait = 3999
    max_wait = 4000
