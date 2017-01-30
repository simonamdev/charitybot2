import requests
from tests.mocks import MockFundraisingWebsite

mocksite = MockFundraisingWebsite(fundraiser_name='justgiving', extra_args=['--debug'])


def setup_module():
    mocksite.start()


def teardown_module():
    mocksite.stop()


class TestMocksite:
    def test_index_page(self):
        response = requests.get('http://127.0.0.1:5000/')
        assert 200 == response.status_code
