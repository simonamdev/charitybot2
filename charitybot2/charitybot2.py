class BaseComponent:
    def __init__(self, tag, verbose=False):
        self.tag = tag
        self.verbose = verbose

    def log(self, log_string, send_to_db=True):
        if self.verbose:
            print('[{0}] {1}'.format(self.tag, log_string))
        if send_to_db:
            self.send_to_db()

    def send_to_db(self):
        pass
