from charitybot2.sources.scraper import Scraper, InvalidFundraiserUrlException, SourceUnavailableException
from charitybot2.storage.logger import Logger


class MyDonateScraper(Scraper):
    def __init__(self, url, scraper_type, debug=False):
        self.url = url
        self.scraper_type = scraper_type
        self.debug = debug
        self.logger = Logger(source='MyDonateScraper', event='', console_only=self.debug)
        try:
            super().__init__(url=self.url, debug=debug)
        except SourceUnavailableException:
            raise InvalidFundraiserUrlException
        self.logger.log_info('MyDonate Scraper URL: {}'.format(self.url))

    def get_type(self):
        return self.scraper_type

    def scrape_amount_raised(self):
        pass


class MyDonateTeamsScraper(MyDonateScraper):
    def __init__(self, url, debug):
        super().__init__(url=url, scraper_type='teams', debug=debug)

    def scrape_amount_raised(self):
        pass


class MyDonateScraperCreator:
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

    def get_scraper(self):
        return self.__determine_scraper_type()

    def __determine_scraper_type(self):
        if 'teams' in self.url:
            return MyDonateTeamsScraper(url=self.url, debug=self.debug)
        else:
            raise InvalidFundraiserUrlException('Unable to figure out fundraiser type from URL')
