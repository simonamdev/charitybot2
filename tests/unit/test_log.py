import pytest
from charitybot2.models.log import Log, LogLevel, InvalidLogLevelException, InvalidLogException

test_log = Log(timestamp=1, level=LogLevel.verbose, source='source', event='event', message='message')


class TestLogInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (1, test_log.timestamp),
        (LogLevel.verbose, test_log.level),
        ('source', test_log.source),
        ('event', test_log.event),
        ('message', test_log.message)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual

    def test_string_version_only_80_characters_long(self):
        print(test_log)
        assert len(str(test_log)) <= 80

    def test_log_with_long_string_gets_truncated_to_80(self):
        big_log = Log(
            timestamp=1,
            level=LogLevel.verbose,
            source='source',
            event='event',
            message='abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
        print(big_log)
        assert len(str(big_log)) == 80


class TestLogExceptions:
    @pytest.mark.parametrize('level', [
        '',
        'bla',
        None,
        [],
        (),
        300061
    ])
    def test_passing_invalid_log_level_throws_exception(self, level):
        with pytest.raises(InvalidLogLevelException):
            test_log = Log(timestamp=1, level=level, source='source', event='event', message='message')

    @pytest.mark.parametrize('timestamp,level,source,event,message', [
        (-1, LogLevel.verbose, 'source', 'event', 'message'),
        (1, LogLevel.verbose, '', 'event', 'message'),
        (1, LogLevel.verbose, 'source', '', 'message'),
        (1, LogLevel.verbose, 'source', 'event', ''),
        (1, LogLevel.verbose, 'source', 'event', None),
        (1, LogLevel.verbose, 'source', None, 'message'),
        (1, LogLevel.verbose, None, 'event', 'message'),
        (None, LogLevel.verbose, 'source', 'event', 'message')
    ])
    def test_passing_invalid_parameters_throws_exception(self, timestamp, level, source, event, message):
        with pytest.raises(InvalidLogException):
            test_log = Log(timestamp=timestamp, level=level, source=source, event=event, message=message)
