import pytest

import charitybot2.sources.scraper as scraper


class TestSoupDataSourceValidity:
    @pytest.mark.parametrize('source_name,tag_type', [
        ('', ''),
        ('foo', ''),
        ('', 'bar'),
        ('foo', 'bar'),
        ('foo', 'h1')
    ])
    def test_passing_invalid_source_name(self, source_name, tag_type):
        sds = scraper.SoupDataSources()
        with pytest.raises(scraper.InvalidSoupSourceNameGiven):
            sds.set_source(source_name=source_name, tag_type=tag_type)

    def test_retrieval_of_passed_parameters(self):
        sds = scraper.SoupDataSources()
        sds.set_source(source_name='amount_raised', tag_type='h3', tag_class='col-md-4', tag_id='youwotm8')
        assert 'h3' == sds.get_source_tag('amount_raised')
        assert 'col-md-4' == sds.get_source_class('amount_raised')
        assert 'youwotm8' == sds.get_source_id('amount_raised')

    def test_setting_id_auto_removes_hashtag(self):
        sds = scraper.SoupDataSources()
        sds.set_source(source_name='amount_raised', tag_type='h1', tag_id='#pythonisawesome')
        assert '#' not in sds.get_source_id('amount_raised')


class TestSoupDataSourceRetrieval:
    def test_getting_nonexistent_source_raises_exception(self):
        sds = scraper.SoupDataSources()
        with pytest.raises(scraper.SoupDataSourceNotRegisteredException):
            sds.get_source_class(source_name='some source')

    def test_getting_list_of_added_sources(self):
        sds = scraper.SoupDataSources()
        assert sds.get_available_source_names() == ()
        sds.set_source(source_name='amount_raised', tag_type='h1')
        assert 'amount_raised' in sds.get_available_source_names()
