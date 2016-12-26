from charitybot2.events.currency import Currency


class EventInvalidException(Exception):
    pass


class EventAlreadyFinishedException(Exception):
    pass


class Event:
    def __init__(self, event_configuration, db_handler):
        self.event_configuration = event_configuration
        self.db_handler = db_handler
        self.amount_raised = 0

    def get_event_name(self):
        return self.event_configuration.get_value('event_name')

    def get_channel_name(self):
        return self.event_configuration.get_value('channel_name')

    def get_start_time(self):
        return self.event_configuration.get_value('start_time')

    def get_end_time(self):
        return self.event_configuration.get_value('end_time')

    def get_target_amount(self):
        return self.event_configuration.get_value('target_amount')

    def get_source_url(self):
        return self.event_configuration.get_value('source_url')

    def get_update_tick(self):
        return self.event_configuration.get_value('update_tick')

    def get_currency(self):
        return Currency(self.event_configuration.get_value('currency'))

    def get_amount_raised(self):
        return self.amount_raised

    def set_amount_raised(self, amount):
        self.amount_raised = amount

    def increment_amount_raised(self, amount_increase):
        self.amount_raised += amount_increase
