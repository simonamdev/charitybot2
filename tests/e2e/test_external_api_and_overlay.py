import time

import requests
from bs4 import BeautifulSoup
from charitybot2.events.event_loop import EventLoop
from charitybot2.paths import mocksite_path, external_api_path
from charitybot2.reporter.external_api.external_api import api_full_url
from charitybot2.sources.mocks.mocksite import mocksite_full_url
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

mocksite = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


external_api = ServiceTest(
    service_name='External_API',
    service_url=api_full_url,
    service_path=external_api_path,
    enter_debug=True)


def setup_module():
    mocksite.start_service()
    external_api.start_service()
    r = requests.get(url=mocksite_full_url + 'reset')
    assert 200 == r.status_code


def teardown_module():
    mocksite.stop_service()
    external_api.stop_service()


class TestOverlay:
    def test_getting_last_donation_amount_on_overlay(self):
        test_event = MockEvent('test', time.time() + 10)
        test_event_loop = EventLoop(event=test_event, debug=True)
        test_event_loop.start()
        response = requests.get(url=api_full_url + 'event/test/overlay')
        assert 200 == response.status_code
        assert '<!DOCTYPE html>' in response.content.decode('utf-8')
        soup = BeautifulSoup(response.content, 'html.parser')
        amount_raised = soup.find('span', {'id': 'amount_raised'}).text.strip()
        assert 250.52 == round(float(amount_raised), 2)
