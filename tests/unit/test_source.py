import pytest
from charitybot2.sources.sources import Source, source_names_supported, InvalidSourceNameException, EmptySourceArgumentException


class TestSourceInitialisationValidity:
    def test_initialise_invalid_source_throws_exception(self):
        with pytest.raises(InvalidSourceNameException):
            s = Source(name='fiodjoijgd', url_name='oijfoijd')

    def test_initialise_source_with_empty_name_throws_exception(self):
        with pytest.raises(EmptySourceArgumentException):
            s = Source(name='', url_name='Disability-North')

    def test_initialise_source_with_empty_url_name_throws_exception(self):
        with pytest.raises(EmptySourceArgumentException):
            s = Source(name='justgiving', url_name='')

    def test_initialise_source_with_valid_source_names(self):
        for source_name in source_names_supported:
            s = Source(name=source_name, url_name='test_url_name')

    def test_retrieve_source_name_and_url_name(self):
        s = Source(name='justgiving', url_name='test_url_name')
        assert s.get_name() == 'justgiving'
        assert s.get_url_name() == 'test_url_name'
