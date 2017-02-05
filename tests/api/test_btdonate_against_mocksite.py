import pytest
from charitybot2.sources.mocks.mocksite import mock_mydonate_teams_url, actual_justgiving_fundraising_url, \
    actual_mydonate_teams_url
from charitybot2.sources.mydonate import MyDonateScraperCreator
from charitybot2.sources.scraper import SourceUnavailableException
from charitybot2.sources.url_call import UrlCall, ConnectionFailedException
from tests.mocks import MockFundraisingWebsite

mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='mydonate')


def try_to_start_mocksite():
    try:
        response = UrlCall(url=mock_fundraising_website.url).get()
        if not response.status_code == 200:
            mock_fundraising_website.start()
    except ConnectionFailedException:
        mock_fundraising_website.start()


def setup_module():
    try_to_start_mocksite()


def teardown_module():
    # Stop the mocksite only if it is still up
    try:
        response = UrlCall(url=mock_fundraising_website.url).get()
        if response.status_code == 200:
            mock_fundraising_website.stop()
    except ConnectionFailedException:
        pass


class TestMyDonateScrapers:
    @pytest.mark.parametrize('url,debug,actual_url,result', [
        (actual_mydonate_teams_url, True, True, ''),
        (mock_mydonate_teams_url, True, False, '£100.52'),
    ])
    def test_getting_amount_raised_with_scrapers(self, url, debug, actual_url, result):
        md = MyDonateScraperCreator(
            url=url,
            debug=debug).get_scraper()
        amount_raised = md.scrape_amount_raised()
        assert amount_raised is not None
        if actual_url:
            assert '.' in amount_raised or ',' in amount_raised
        else:
            assert amount_raised == result


class TestMyDonateScraperFailure:
    def test_get_amount_raised_fails_gracefully(self):
        try_to_start_mocksite()
        md = MyDonateScraperCreator(
            url=mock_mydonate_teams_url,
            debug=True).get_scraper()
        # simulate as if the website went down
        mock_fundraising_website.stop()
        with pytest.raises(SourceUnavailableException):
            amount_raised = md.scrape_amount_raised()
