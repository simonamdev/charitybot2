from smokesignal import smokesignal


class Scraper:
    def __init__(self, url, verbose=False):
        self.url = url
        self.get = smokesignal.GetRequest(url=url, verbose=verbose)

    def is_url_valid(self):
        self.get.make_request()
        return self.get.get_response_code() == 200

    def get_url_contents(self):
        self.get.make_request()
        return self.get.get_response_contents()
