import requests
import random

from charitybot2.paths import user_agents_file_path


class ConnectionFailedException(Exception):
    pass


class UrlCall:
    def __init__(self, url, params=None, headers=None, timeout=2):
        self.url = url
        self.params = params if params is not None else {}
        self.headers = headers if headers is not None else {}
        self.user_agent = return_random_user_agent()
        self.timeout = timeout

    def make_request(self, request_function):
        try:
            return request_function()
        except TimeoutError:
            raise ConnectionFailedException('Connection to {} timed out'.format(self.url))
        except requests.exceptions.ConnectionError:
            raise ConnectionFailedException('Failed to establish a connection to: {}'.format(self.url))
        except requests.exceptions.TooManyRedirects:
            raise ConnectionFailedException('Too many redirects when connecting to: {}'.format(self.url))
        except requests.exceptions.MissingSchema:
            raise ConnectionFailedException('No schema passed for the url: {}'.format(self.url))

    def get(self):
        self.headers.update({'User-Agent': self.user_agent})
        return self.make_request(
            request_function=lambda: requests.get(
                url=self.url,
                headers=self.headers,
                params=self.params,
                timeout=self.timeout))


def return_random_user_agent():
    with open(user_agents_file_path, 'r') as user_agent_file:
        user_agent = random.choice(user_agent_file.readlines())
    return user_agent.strip()
