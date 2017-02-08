from urllib.parse import urljoin

from charitybot2.paths import user_agents_file_path
from charitybot2.sources.url_call import UrlCall
from tests.mocks import MockFundraisingWebsite

mock_fundraising_website = MockFundraisingWebsite(fundraiser_name='justgiving')


def setup_module():
    mock_fundraising_website.start()


def teardown_module():
    mock_fundraising_website.stop()


def get_all_user_agent_strings():
    with open(user_agents_file_path, 'r') as user_agents_file:
        user_agents = [row.strip() for row in user_agents_file.readlines()]
    return user_agents


class TestUrlCall:
    user_agents = get_all_user_agent_strings()

    def test_for_different_user_agents(self):
        url_call = UrlCall(url=urljoin(mock_fundraising_website.url, 'useragent'))
        response = url_call.get()
        used_user_agent = response.content.decode('utf-8')
        print(used_user_agent)
        assert used_user_agent in self.user_agents

    def test_several_user_agents(self):
        for i in range(0, 500):
            self.test_for_different_user_agents()
