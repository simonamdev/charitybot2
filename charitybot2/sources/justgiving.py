import json
import requests

from charitybot2.models.donation import Donation


class JustGivingFundraisingSource:
    url = 'https://api.justgiving.com/v1/fundraising/pages/{}/donations'

    def __init__(self, event_identifier, page_short_name, api_key, limit=25):
        self._event_identifier = event_identifier
        self._page_short_name = page_short_name
        self._page_size = limit
        self._api_key = api_key
        self._headers = {
            'x-api-key': api_key,
            'Accept': 'application/json'
        }
        self._limit = limit

    def get_new_donations(self, known_donation_ids=()):
        donation_pages = self.request_donations_from_api()
        all_donations = []
        for donations in donation_pages:
            donations = [donation for donation in donations if str(donation['id']) not in known_donation_ids]
            if len(donations) == 0:
                break
            all_donations.extend(donations)
        return [self._convert_to_donation(donation) for donation in all_donations]

    def get_all_donations(self):
        donation_pages = self.request_donations_from_api()
        all_donations = []
        for donations in donation_pages:
            all_donations.extend(donations)
        return [self._convert_to_donation(donation) for donation in all_donations]

    def request_donations_from_api(self):
        # Get the first page to determine pagination
        data = self.get_donations_page(page=1)
        yield data['donations']
        for i in range(2, data['pagination']['totalPages'] + 1):
            data = self.get_donations_page(page=i)
            yield data['donations']

    def get_donations_page(self, page=1):
        response = requests.get(
            url=self.url.format(self._page_short_name) + '?pageSize={}&pageNum={}'.format(self._page_size, page),
            headers=self._headers)
        if not 200 == response.status_code:
            print(response.status_code)
            print(response.text)
        else:
            return json.loads(response.text)

    def _convert_to_donation(self, donation):
        # /Date(1505495742000+0000)/
        return Donation(
            amount=donation['amount'],
            event_identifier=self._event_identifier,
            timestamp=int(donation['donationDate'].split('(')[1].split('+')[0]) // 1000,
            external_reference=str(donation['id']),
            donor_name=donation['donorDisplayName'],
            notes=donation['message']
        )

if __name__ == '__main__':
    source = JustGivingFundraisingSource(event_identifier='onespecialday2017', page_short_name='elite-aid', api_key='bla', limit=25)
    donations = source.get_all_donations()
    print(donations)
    print(len(donations))
    new_donations = source.get_new_donations(known_donation_ids=['1009835731'])
    print(new_donations)
    print(len(new_donations))
