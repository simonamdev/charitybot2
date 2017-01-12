import pytest
from bs4 import BeautifulSoup
from charitybot2.paths import mocksite_path
from charitybot2.sources.scraper import Scraper, SourceUnavailableException
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.tests import ServiceTest

url = MockEvent.mocksite_base_url
mocksite = ServiceTest(
    service_name='Donations Mocksite',
    service_url=url,
    service_path=mocksite_path,
    enter_debug=False)


def setup_module():
    mocksite.start_service()


def teardown_module():
    mocksite.stop_service()


class TestScraperURLValidity:
    def test_get_bytes_content(self):
        scraper = Scraper(url=url, debug=True)
        content = scraper.get_data_from_url().content
        assert isinstance(content, bytes)

    def test_non_empty_url_contents(self):
        scraper = Scraper(url=url, debug=True)
        content = scraper.get_contents_from_url()
        assert '<!DOCTYPE html>' in content


class TestScraperSourceValidity:
    def test_non_available_source_exception(self):
        with pytest.raises(SourceUnavailableException):
            scraper = Scraper(url='http://34242.3435345.33443.1:3434', debug=True)
            scraper.get_data_from_url()

    def test_soup_valid_url_returns_bs4_object(self):
        s = Scraper(url=url, debug=True)
        soup = s.get_soup_from_url()
        assert isinstance(soup, type(BeautifulSoup('<h1>something</h1>', 'lxml')))
