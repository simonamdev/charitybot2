import os
import charitybot2.events.events as events
import charitybot2.events.event_config as event_config

current_directory = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_directory, 'configs', 'valid_config' + '.' + event_config.EventConfiguration.config_format)

