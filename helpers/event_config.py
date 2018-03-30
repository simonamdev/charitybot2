import copy

from charitybot2.creators.event_configuration_creator import EventConfigurationCreator

test_event_config_values = {
    'identifier': 'test',
    'title': 'CB Test Event',
    'start_time': 0,
    'end_time': 1,
    'target_amount': 100,
    'update_delay': 5,
    'currency_key': 'EUR',
    'source_details': {
        'source': 'TEST',
        'url': 'http://www.charitybot.net'
    }
}


test_justgiving_event_config_values = copy.deepcopy(test_event_config_values)
test_justgiving_event_config_values['source_details']['source'] = 'JUSTGIVING'
test_justgiving_event_config_values['source_details']['page_short_name'] = 'TEST'


def get_updated_test_config_values(updated_values=None):
    valid_config_values = copy.deepcopy(test_event_config_values)
    if updated_values is not None:
        valid_config_values.update(updated_values)
    return valid_config_values


def get_test_event_configuration(updated_values=None):
    test_event_configuration_creator = EventConfigurationCreator(
        configuration_values=get_updated_test_config_values(updated_values=updated_values))
    return test_event_configuration_creator.configuration
