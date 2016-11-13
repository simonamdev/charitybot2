from charitybot2.paths import mocksite_path
from selenium import webdriver
from tests.e2e.test_reporter_twitch import navigate_to_twitch_channel
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

driver = None
service_test = ServiceTest(
    service_name='Donations Mocksite',
    service_url=MockEvent.mocksite_base_url,
    service_path=mocksite_path,
    enter_debug=False)


def setup_module():
    service_test.start_service()
    global driver
    driver = webdriver.Chrome()
    driver.implicity_wait(5)


def teardown_module():
    service_test.stop_service()
    global driver
    driver.close()


class TestFullTwitchEvent:
    navigate_to_twitch_channel()
    


class TestFullAPIEvent:
    pass
