import json
import os

from charitybot2.paths import cb2_justgiving_api_key_path, debug_justgiving_api_key_path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as selenium_exceptions

from charitybot2.sources.url_call import ConnectionFailedException, return_random_user_agent, UrlCall
from charitybot2.storage.logger import Logger

from .scraper import Scraper, SoupDataSources, SourceUnavailableException, ScraperException


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
        self.driver = None
        self.tries = 0
        # self.__setup_driver()

    def __setup_driver(self):
        # Set User Agent
        caps = DesiredCapabilities.PHANTOMJS
        caps['phantomjs.page.settings.userAgent'] = (return_random_user_agent())
        caps['phantomjs.page.settings.loadImages'] = False
        caps['phantomjs.page.settings.resourceTimeout'] = 10000
        self.driver = webdriver.PhantomJS(service_log_path=os.path.devnull, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'], desired_capabilities=caps)
        # Set timeout
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(10)
        # print(self.driver.execute_script('return navigator.userAgent', ''))

    def scrape_amount_raised(self):
        # retries = 0
        # while retries < 3:
        #     try:
        #         amount_raised
        #     except:
        #         pass
        self.__setup_driver()
        amount_raised = self.__get_amount_raised()
        self.driver.quit()
        return amount_raised

    def __get_amount_raised(self):
        # if self.debug:
        #     print('Accessing {} with driver'.format(self.url))
        self.tries = 0
        while self.tries < 3:
            try:
                self.__try_to_access_page()
                self.tries = 3
            except selenium_exceptions.TimeoutException:
                self.tries += 1
                print('Current tries: {}'.format(self.tries))
                print('Restarting driver')
                self.driver.quit()
                self.__setup_driver()
        # self.driver.get(self.url.replace('https', 'http'))
        script_tags = self.driver.find_elements_by_tag_name('script')
        # if self.debug:
        #     print(script_tags)
        # searching method uncovered index 11, however it might need more testing later on
        # return self.__search_for_script_tag(script_tags=script_tags)
        # return self.__parse_script_tag_for_amount_raised(script_tags[11])
        return self.__parse_script_tag_for_amount_raised(self.__search_for_script_tag(script_tags=script_tags))

    def __try_to_access_page(self):
        self.driver.get(self.url)

    @staticmethod
    def __search_for_script_tag(script_tags):
        script_tag = ''
        for script in script_tags:
            inner_html = script.get_attribute('innerHTML').strip()
            first_part = inner_html[0:9]
            if 'window.JG' == first_part and not first_part == '':
                print('Tag Index from search: {}'.format(script_tags.index(script)))
                script_tag = script
                break
        return script_tag

    def __parse_script_tag_for_amount_raised(self, script_tag):
        inner_html = script_tag.get_attribute('innerHTML').strip()
        # while inner_html == '':
        #     print('Entering recursive attempt to get amount raised')
        #     script_tags = self.driver.find_elements_by_tag_name('script')
        #     script_tag = self.__search_for_amount_raised(script_tags=script_tags)
        #     inner_html = script_tag.get_attribute('innerHTML').strip()
        # this is required to allow the mock test to pass
        if not inner_html[0] == '{':
            inner_html = inner_html[59:-1]
        parsed_html = json.loads(inner_html)
        currency_symbol = parsed_html['campaign']['totalRaisedInPageCurrency']['currency']['symbol']
        amount_raised = str(parsed_html['campaign']['totalRaisedInPageCurrency']['value'])
        return currency_symbol + amount_raised


class JustGivingAPIScraper(JustGivingScraper):
    def __init__(self, url, debug):
        super().__init__(url=url, scraper_type='api', debug=debug)
        self.api_key_file_path = debug_justgiving_api_key_path if debug else cb2_justgiving_api_key_path
        self.api_key = None
        self.__initialise_scraper()

    def __initialise_scraper(self):
        self.api_key = self.__get_api_key_from_file()

    def __get_api_key_from_file(self):
        with open(self.api_key_file_path, 'r') as api_key_file:
            api_key = api_key_file.read()
        self.__validate_api_key(api_key=api_key)
        return api_key

    def __validate_api_key(self, api_key):
        try:
            assert len(api_key) == 8
            assert str.isalnum(api_key)
        except AssertionError:
            raise ScraperException('Unable to retrieve a valid JustGiving API key from the given path: {}'.format(
                self.api_key_file_path))

    def scrape_amount_raised(self):
        api_call_headers = {
            'x-api-key': self.api_key,
            'Accept': 'application/json'
        }
        url_call = UrlCall(url=self.url, headers=api_call_headers, timeout=5)
        try:
            response = url_call.get()
        except ConnectionFailedException:
            raise SourceUnavailableException
        try:
            response = json.loads(response.content.decode('utf-8'))
        except ValueError:
            self.logger.log_error('Unable to parse returned data from source')
            raise SourceUnavailableException
        if isinstance(response, list):
            self.logger.log_error('Irregular response received: {}'.format(response))
            raise SourceUnavailableException
        return response['totalRaised']


class JustGivingScraperCreator:
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

    def get_scraper(self):
        return self.__determine_scraper_type()

    def __determine_scraper_type(self):
        if 'api' in self.url:
            return JustGivingAPIScraper(url=self.url, debug=self.debug)
        elif 'fundraising' in self.url:
            return JustGivingFundraisingScraper(url=self.url, debug=self.debug)
        elif 'campaign' in self.url:
            return JustGivingCampaignScraper(url=self.url, debug=self.debug)
        else:
            raise InvalidFundraiserUrlException('Unable to discern fundraiser type from the JustGiving URL')
