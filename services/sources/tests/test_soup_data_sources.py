from scraper import scraper
import pytest


def test_retrieval_of_passed_parameters():
    sds = scraper.SoupDataSources()
    sds.set_source(source_name='amount_raised', tag_type='h3', tag_class='col-md-4', tag_id='youwotm8')
    assert 'h3' == sds.get_source_tag('amount_raised')
    assert 'col-md-4' == sds.get_source_class('amount_raised')
    assert 'youwotm8' == sds.get_source_id('amount_raised')


def test_setting_id_auto_removes_hashtag():
    sds = scraper.SoupDataSources()
    sds.set_source(source_name='amount_raised', tag_type='h1', tag_id='#pythonisawesome')
    assert '#' not in sds.get_source_id('amount_raised')


def test_getting_nonexistent_source_raises_exception():
    sds = scraper.SoupDataSources()
    with pytest.raises(scraper.SoupDataSourceNotRegisteredException):
        sds.get_source_class(source_name='some source')


def test_getting_list_of_added_sources():
    sds = scraper.SoupDataSources()
    assert sds.get_available_source_names() == ()
    sds.set_source(source_name='amount_raised', tag_type='h1')
    assert 'amount_raised' in sds.get_available_source_names()


def test_passing_invalid_source_name():
    sds = scraper.SoupDataSources()
    with pytest.raises(scraper.InvalidSoupSourceNameGiven):
        sds.set_source(source_name='test', tag_type='h1')

