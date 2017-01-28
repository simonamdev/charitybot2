import pytest
from charitybot2.models.currency import Currency
from charitybot2.models.event import Event

test_event_currency = Currency(key='USD')
test_event = Event()


# class TestEventInstantiation:
#     @pytest.mark.parametrize('expected,actual', [
#         ('identifier', test_event.identifier),
#         ('title', test_event.title),
#         (0, test_event.start_time),
#         (1, test_event.end_time),
#         (0, test_event.starting_amount),
#         (100, test_event.amount_raised),
#         (5, test_event.update_delay),
#         (test_event_currency.key, test_event.currency.key)
#     ])
#     def test_retrieval(self, expected, actual):
#         assert expected == actual
