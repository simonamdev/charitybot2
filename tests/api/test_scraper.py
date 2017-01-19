import pytest
from bs4 import BeautifulSoup
from charitybot2.paths import mocksite_path
from charitybot2.sources.scraper import Scraper, SourceUnavailableException
from tests.integration.test_event_loop_with_mocksite import MockEvent
from tests.mocks import ServiceTest

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

valid_scraper = Scraper(url=url, debug=True)


class TestScraperURLValidity:
    def test_get_bytes_content(self):
        content = valid_scraper.get_data_from_url().content
        assert isinstance(content, bytes)

    def test_non_empty_url_contents(self):
        content = valid_scraper.get_contents_from_url()
        assert '<!DOCTYPE html>' in content

    def test_url_validation_for_valid_url(self):
        assert True is valid_scraper.validate_url()

    def test_url_validation_for_invalid_url(self):
        invalid_scraper = Scraper(url='http://blablalba.blablabla', debug=True)
        assert False is invalid_scraper.validate_url()


class TestScraperSourceValidity:
    def test_non_available_source_exception(self):
        with pytest.raises(SourceUnavailableException):
            scraper = Scraper(url='http://34242.3435345.33443.1:3434', debug=True)
            scraper.get_data_from_url()

    def test_soup_returns_from_basic_html(self):
        soup = valid_scraper.get_soup(url_contents='<html><body><h1>Test HTML</h1></body></html>')
        assert isinstance(soup, BeautifulSoup)

    def test_soup_valid_url_returns_bs4_object(self):
        soup = valid_scraper.get_soup_from_url()
        assert isinstance(soup, BeautifulSoup)
