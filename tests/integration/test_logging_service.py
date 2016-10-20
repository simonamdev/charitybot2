import requests

from charitybot2.storage.logging_service import service_url, service_port

service_full_url = 'http://' + service_url + ':' + str(service_port) + '/'

print(service_full_url)


class TestLoggingServiceResponse:
    def test_service_responds_with_name(self):
        response = requests.get(url=service_full_url)
        assert 'Logging Service' == response.content.decode('utf-8')
