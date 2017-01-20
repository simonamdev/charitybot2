import os

from selenium import webdriver

from charitybot2.sources.url_call import ConnectionFailedException
from charitybot2.storage.logger import Logger

from .scraper import Scraper, SoupDataSources, SourceUnavailableException


class NoFundraiserNameGivenException(Exception):
    pass


class InvalidFundraiserUrlException(Exception):
    pass


class JustGivingScraper(Scraper):
    def __init__(self, url, scraper_type, debug=False):
        self.url = url
        self.scraper_type = scraper_type
        self.debug = debug
        self.logger = Logger(source='JustGivingScraper', event='', console_only=self.debug)
        self.soup_data_sources = None
        try:
            super().__init__(url=self.url, debug=debug)
        except SourceUnavailableException:
            raise InvalidFundraiserUrlException
        self.logger.log_info('JustGiving Scraper URL: {}'.format(self.url))

    def get_type(self):
        return self.scraper_type

    def scrape_amount_raised(self):
        pass


class JustGivingFundraisingScraper(JustGivingScraper):
    def __init__(self, url, debug):
        super().__init__(url=url, scraper_type='fundraising', debug=debug)
        self.soup_data_sources = self.__setup_soup_data_sources()

    def __setup_soup_data_sources(self):
        sds = SoupDataSources()
        sds.set_source(
            source_name='amount_raised',
            tag_type='span',
            tag_class='statistics-amount-raised theme-highlight-text-font')
        self.logger.log_info('JustGiving Fundraising Scraper initialised with: {0} sources'.format(
            len(sds.get_available_source_names())))
        return sds

    def __get_source_value_from_url_contents(self, url_contents, source_name):
        try:
            source_value = self.get_soup(url_contents=url_contents).find(
                self.soup_data_sources.get_source_tag(source_name=source_name),
                self.soup_data_sources.get_bs4_find_parameters_dict(source_name=source_name)
            ).text
        except AttributeError:
            self.logger.log_error('Unable to find amount raised on Justgiving source')
            raise SourceUnavailableException('Unable to find amount raised on JustGiving website')
        return source_value

    def __get_source_value(self, source_name):
        try:
            url_contents = self.get_contents_from_url()
            source_value = self.__get_source_value_from_url_contents(url_contents=url_contents, source_name=source_name)
        except ConnectionFailedException:
            self.logger.log_error('Unable to connect to the scraper source')
            raise SourceUnavailableException('Unable to connect to the source')
        return source_value

    def scrape_amount_raised(self):
        return self.__get_source_value(source_name='amount_raised')


class JustGivingCampaignScraper(JustGivingScraper):
    def __init__(self, url, debug):
        super().__init__(url=url, scraper_type='campaign', debug=debug)
        self.logger.log_info('Starting up PhantomJS driver (this may take some time)')
        self.driver = webdriver.PhantomJS(service_log_path=os.path.devnull)

    def __get_amount_raised(self):
        self.driver.get(self.url)
        element = self.driver.find_element_by_css_selector(
            '.dna-text-brand-l.jg-theme-text.TotalDonation__totalRaised___1sUPY')
        return element.text

    def scrape_amount_raised(self):
        return self.__get_amount_raised()


class JustGivingScraperCreator:
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

    def get_scraper(self):
        return self.__determine_scraper_type()

    def __determine_scraper_type(self):
        if 'fundraising' in self.url:
            return JustGivingFundraisingScraper(url=self.url, debug=self.debug)
        elif 'campaign' in self.url:
            return JustGivingCampaignScraper(url=self.url, debug=self.debug)
        else:
            raise InvalidFundraiserUrlException('Unable to discern fundraiser type from the JustGiving URL')
