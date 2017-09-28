import json

import requests

from pprint import pprint

api_key = 'example'
charity_name = 'specialeffect'
campaign_name = 'onespecialday2017'
page_size = 5

url = 'https://api.justgiving.com'
# donation_url = url + '/v1/campaigns/{}/{}'.format(charity_name, campaign_name)


def get_donation_url(page_number):
    return url + '/v1/fundraising/pages/{}/donations?pageNum={}&pageSize=6'.format(
        'onespecialdayfootballchallenge',
        page_number,
        page_size
    )

headers = {
    'x-api-key': api_key,
    'Accept': 'application/json'
}

response = requests.get(url=get_donation_url(1), headers=headers)
print('Page 1')
print(response.status_code)
data = json.loads(response.text)
pprint(data['donations'])
pprint(data['pagination'])

donation_results = data['donations']
# get all results from all pages
page_count = data['pagination']['totalPages']
if page_count >= 2:
    for i in range(2, page_count + 1):
        print('Page {}'.format(i))
        response = requests.get(url=get_donation_url(i), headers=headers)
        print(response.url)
        print(response.status_code)
        data = json.loads(response.text)
        pprint(data['pagination'])
        pprint(data['donations'])
        donation_results.extend(data['donations'])

pprint(len(donation_results))
pprint(donation_results)
pprint([donation['donorDisplayName'] for donation in donation_results])
