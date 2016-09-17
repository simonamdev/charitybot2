from scraper import scraper
import pytest


def test_retrieval_of_passed_paramters():
    sds = scraper.SoupDataSources()
    sds.set_source(source_name='test', tag_type='h3', tag_class='col-md-4', tag_id='youwotm8')
    assert 'test' in sds.get_available_source_names()
    assert 'h3' == sds.get_source_tag('test')
    assert 'col-md-4' == sds.get_source_class('test')
    assert 'youwotm8' == sds.get_source_id('test')


def test_setting_id_auto_removes_hashtag():
    sds = scraper.SoupDataSources()
    sds.set_source(source_name='test', tag_type='h1', tag_id='#pythonisawesome')
    assert '#' not in sds.get_source_id('test')


def test_getting_nonexistent_source_raises_exception():
    sds = scraper.SoupDataSources()
    with pytest.raises(scraper.SoupDataSourceNotRegisteredException):
        sds.get_source_class(source_name='some source')


def test_getting_list_of_added_sources():
    sds = scraper.SoupDataSources()
    assert sds.get_available_source_names() == ()
    sds.set_source(source_name='test', tag_type='h1')
    assert 'test' in sds.get_available_source_names()
