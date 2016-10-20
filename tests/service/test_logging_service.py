import requests

from charitybot2.storage.logging_service import service_url, service_port

service_full_url = 'http://' + service_url + ':' + str(service_port) + '/'
print('Microservice URL is: {}'.format(service_full_url))


class TestLoggingServiceResponse:
    def test_service_returns_200_and_responds_with_name_on_base_url(self):
        response = requests.get(url=service_full_url)
        assert 200 == response.status_code
        assert 'Logging Service' == response.content.decode('utf-8')

    def test_service_returns_200_with_health_check(self):
        response = requests.get(url=service_full_url + 'health')
        print(response.content)
        assert 200 == response.status_code
