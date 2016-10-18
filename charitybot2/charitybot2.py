class BaseComponent:
    def __init__(self, tag, verbose=False):
        self.tag = tag
        self.verbose = verbose

    def log(self, log_string):
        if self.verbose:
            print('[{0}] {1}'.format(self.tag, log_string))
