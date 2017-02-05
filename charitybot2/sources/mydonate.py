from charitybot2.sources.scraper import Scraper, InvalidFundraiserUrlException


class MyDonateScraper(Scraper):
    pass


class MyDonateTeamsScraper(MyDonateScraper):
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
