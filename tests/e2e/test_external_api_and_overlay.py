from charitybot2.paths import mocksite_path
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


class TestExternalAPI:
    def test_getting_last_donation(self):
        pass