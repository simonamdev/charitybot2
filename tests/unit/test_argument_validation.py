from charitybot2.start_bot import setup_argument_parser

parser = setup_argument_parser()


class TestParserFlagOptions:
    def test_debug_flag(self):
        parsed = parser.parse_args(['--debug'])
        assert True is parsed.debug
