import random
from time import sleep

import pytest
from bs4 import BeautifulSoup
from charitybot2.api_calls.private_api_calls import PrivateApiCalls
from charitybot2.models.donation import Donation
from charitybot2.paths import console_script_path, private_api_script_path
from charitybot2.private_api.private_api import private_api_service
from charitybot2.public_api.console.console import app
from charitybot2.sources.url_call import UrlCall
from charitybot2.start_service import Service, ServiceRunner
from faker import Faker
from selenium.webdriver.common.keys import Keys
from tests.setup_test_database import setup_test_database
from selenium import webdriver


driver = None
test_event_identifier = 'test'
private_api_calls = PrivateApiCalls(base_api_url=private_api_service.full_url)


console_service = Service(
    name='Test Console',
    app=app,
    address='127.0.0.1',
    port=5000,
    debug=True)
console_service_runner = ServiceRunner(
    service=console_service,
    file_path=console_script_path,
    start_delay=1,
    stop_delay=1)

api_service = Service(
    name='Test Private API',
    app=app,
    address='127.0.0.1',
    port=8001,
    debug=True)
api_service_runner = ServiceRunner(
    service=api_service,
    file_path=private_api_script_path,
    start_delay=1,
    stop_delay=1)


def setup_module():
    # setup_test_database()
    console_service_runner.run()
    api_service_runner.run()
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)


def teardown_module():
    console_service_runner.stop_running()
    api_service_runner.stop_running()
    global driver
    driver.close()

test_event_url = console_service.full_url + 'event/{}/'.format(test_event_identifier)


class TestConsolePaths:
    @pytest.mark.parametrize('url', [
        console_service.full_url,
        test_event_url
    ])
    def test_paths_return_200(self, url):
        response = UrlCall(url=url).get()
        assert 200 == response.status_code


def get_soup_text_by_id(tag_id):
    global driver
    return BeautifulSoup(driver.find_element_by_id(tag_id).text.strip(), 'html.parser').text


# Helper methods to get data from the page
def get_total_raised():
    driver.get(test_event_url)
    sleep(1)
    total_raised = get_soup_text_by_id('donation-total')
    return total_raised


def get_donation_table_rows():
    driver.get(test_event_url)
    sleep(1)
    donations_table_body = driver.find_element_by_id('donations-table-body')
    donations_table_body_text = BeautifulSoup(donations_table_body.text.strip(), 'html.parser')
    if donations_table_body_text == '':
        return []
    table_rows = donations_table_body.find_elements_by_tag_name('tr')
    return [convert_web_element_to_donation_dict(row) for row in table_rows]


def convert_web_element_to_donation_dict(web_element):
    # break up the tr into separate tds
    row_tds = web_element.find_elements_by_tag_name('td')
    return dict(
        amount=row_tds[1].text.strip(),
        timestamp=row_tds[2].text.strip(),
        donor=row_tds[3].text.strip(),
        notes=row_tds[4].text.strip(),
        external_reference=row_tds[5].text.strip(),
        internal_reference=row_tds[6].text.strip())


def submit_api_donation(amount, donor, notes):
    donation = Donation(
        amount=amount,
        event_identifier=test_event_identifier,
        donor_name=donor,
        notes=notes)
    private_api_calls.register_donation(donation=donation)
    sleep(1)


def submit_form_donation(amount, donor, notes, navigate_to_page=True):
    if navigate_to_page:
        driver.get(test_event_url)
        sleep(1)
    # enter info in the form
    enter_donation_into_form(amount, donor, notes)
    # Submit the form
    submit_form()
    sleep(1)


def enter_donation_into_form(amount, donor, notes):
    form = driver.find_element_by_id('new-donation-amount')
    form.send_keys(str(amount))
    form = driver.find_element_by_id('new-donation-donor')
    form.send_keys(str(donor))
    if notes is not None:
        form = driver.find_element_by_id('new-donation-notes')
        form.send_keys(str(notes))


def submit_form():
    form_submit = driver.find_element_by_id('donation-submit-button')
    form_submit.send_keys(Keys.ENTER)


def generate_test_donation_data(count=5):
    fake = Faker()
    test_donations = []
    for i in range(0, count):
        test_amount = round(random.uniform(1.0, 100.0), 2)
        test_name = fake.name()
        test_notes = fake.text()[0:10].strip()
        donation = dict(amount=test_amount, name=test_name, notes=test_notes)
        test_donations.append(donation)
    return test_donations


class TestDonationSubmission:
    def test_total_is_zero_with_no_rows(self):
        setup_test_database(donation_count=0)
        # make sure there are no rows
        assert 0 == len(get_donation_table_rows())
        # make sure the total is 0
        assert '0' == get_total_raised()

    def test_donation_from_api(self):
        setup_test_database(donation_count=0)
        test_amount = random.uniform(1.5, 50.3)
        test_donor = 'Cat'
        test_notes = 'Catnip'
        submit_api_donation(
            amount=test_amount,
            donor=test_donor,
            notes=test_notes)
        rows = get_donation_table_rows()
        assert 1 == len(rows)
        donation_row = rows[0]
        assert round(test_amount, 2) == float(donation_row['amount'].replace('€', ''))
        assert test_donor == donation_row['donor']
        assert test_notes == donation_row['notes']

    def test_several_donations_from_api(self):
        setup_test_database(donation_count=0)
        donation_count = 5
        test_donations = generate_test_donation_data(count=donation_count)
        for i in range(0, donation_count):
            test_donation = test_donations[i]
            submit_api_donation(
                amount=test_donation['amount'],
                donor=test_donation['name'],
                notes=test_donation['notes'])
        test_donations.reverse()
        rows = get_donation_table_rows()
        assert donation_count == len(rows)
        for i in range(0, donation_count):
            current_test_donation = test_donations[i]
            donation_row = rows[i]
            assert round(current_test_donation['amount'], 2) == float(donation_row['amount'].replace('€', ''))
            assert current_test_donation['name'] == donation_row['donor']
            assert current_test_donation['notes'] == donation_row['notes']

    def test_several_donations_from_form(self):
        setup_test_database(donation_count=0)
        donation_count = 5
        test_donations = generate_test_donation_data(count=donation_count)
        # go to the page
        driver.get(test_event_url)
        sleep(1)
        for i in range(0, donation_count):
            test_donation = test_donations[i]
            submit_form_donation(
                amount=test_donation['amount'],
                donor=test_donation['name'],
                notes=test_donation['notes'],
                navigate_to_page=False)
        test_donations.reverse()
        rows = get_donation_table_rows()
        assert donation_count == len(rows)
        for i in range(0, donation_count):
            current_test_donation = test_donations[i]
            donation_row = rows[i]
            assert round(current_test_donation['amount'], 2) == float(donation_row['amount'].replace('€', ''))
            assert current_test_donation['name'] == donation_row['donor']
            assert current_test_donation['notes'] == donation_row['notes']

    def test_donation_through_form(self):
        setup_test_database(donation_count=0)
        test_amount = random.uniform(25.5, 75.3)
        test_donor = 'Dog'
        test_notes = 'Treats'
        submit_form_donation(test_amount, test_donor, test_notes)
        rows = get_donation_table_rows()
        assert 1 == len(rows)
        donation_row = rows[0]
        assert round(test_amount, 2) == float(donation_row['amount'].replace('€', ''))
        assert test_donor == donation_row['donor']
        assert test_notes == donation_row['notes']

    def test_donating_through_api_and_form(self):
        setup_test_database(donation_count=0)
        test_form_donation_amount = 33.2
        test_form_donation_donor = 'Blogger'
        test_form_donation_notes = 'Wolololololo'

        submit_form_donation(
            test_form_donation_amount,
            test_form_donation_donor,
            test_form_donation_notes)

        test_api_donation_amount = 10.5
        test_api_donation_donor = 'Joe'
        test_api_donation_notes = 'Joe is awesome'

        submit_api_donation(
            test_api_donation_amount,
            test_api_donation_donor,
            test_api_donation_notes)

        rows = get_donation_table_rows()
        assert 2 == len(rows)
        # ordered from latest to oldest, so API donation should be first

        api_donation_row = rows[0]
        assert round(test_api_donation_amount, 2) == float(api_donation_row['amount'].replace('€', ''))
        assert test_api_donation_donor == api_donation_row['donor']
        assert test_api_donation_notes == api_donation_row['notes']

        # now check the form donation

        form_donation_row = rows[1]
        assert round(test_form_donation_amount, 2) == float(form_donation_row['amount'].replace('€', ''))
        assert test_form_donation_donor == form_donation_row['donor']
        assert test_form_donation_notes == form_donation_row['notes']

    def test_several_mixed_donations(self):
        setup_test_database(donation_count=0)
        donation_count = 20
        # generate donation data
        test_donations = generate_test_donation_data(count=donation_count)
        # submit donations as either api or form
        for i in range(0, donation_count):
            # True: API
            # False: Form
            test_donation = test_donations[i]
            if random.choice((True, False)):
                submit_api_donation(
                    test_donation['amount'],
                    test_donation['name'],
                    test_donation['notes'])
            else:
                submit_form_donation(
                    test_donation['amount'],
                    test_donation['name'],
                    test_donation['notes'])
        # reverse the donation list since the last one is the latest
        test_donations.reverse()
        sleep(1)
        rows = get_donation_table_rows()
        assert donation_count == len(rows)
        for i in range(0, donation_count):
            current_test_donation = test_donations[i]
            donation_row = rows[i]
            assert round(current_test_donation['amount'], 2) == float(donation_row['amount'].replace('€', ''))
            assert current_test_donation['name'] == donation_row['donor']
            assert current_test_donation['notes'] == donation_row['notes']
