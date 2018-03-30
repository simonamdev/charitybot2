from charitybot2.configurations.event_configuration import EventConfiguration


class JustGivingEventConfiguration(EventConfiguration):
    @property
    def page_short_name(self):
        return self._configuration_values['source_details']['page_short_name']
