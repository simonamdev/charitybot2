import pytest
from bs4 import BeautifulSoup

import charitybot2.sources.scraper as scraper

url = 'https://www.github.com'


class TestScraperURLValidity:
    def test_url_is_valid(self):
        s = scraper.Scraper(url=url, verbose=True)
        assert s.url_is_valid is True

    def test_non_empty_url_contents(self):
        s = scraper.Scraper(url=url, verbose=True)
        s.get_url_contents()
        contents = s.url_contents
        assert '<!DOCTYPE html>' in contents


class TestScraperSourceValidity:
    def test_non_available_source_exception(self):
        with pytest.raises(scraper.SourceUnavailableException):
            s = scraper.Scraper(url='http://iojiowfjiojwiodjfowjdiojviunsduiv', verbose=True)

    def test_soup_valid_url_returns_bs4_object(self):
        s = scraper.Scraper(url=url, verbose=True)
        soup = s.get_soup()
        assert isinstance(soup, type(BeautifulSoup('<h1>something</h1>', 'lxml')))
