from charitybot2.persistence.logger import Logger


class ConsoleLogger(Logger):
    def log(self, log):
        print(str(log))
