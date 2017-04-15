import pytest
from charitybot2.exceptions import IllegalArgumentException
from type_assertions import assert_types, assert_type

integer = 5
real = 0.5
word_string = "hello my name is"


class TestTypeAssertion:
    @pytest.mark.parametrize('variable,type,message', [
        (real, int, "Must be Integer"),
        (word_string, float, "Must be float"),
        (integer, str, "Must be string")
    ])
    def test_passing_invalid_parameters_throws_exception(self, variable, type, message):
        with pytest.raises(IllegalArgumentException):
            assert_type(variable=variable, variable_type=type, exception_message=message)

    def test_passing_several_invalid_parameters_throws_exception(self):
        all_at_once = (
            (integer, int, "Must be Integer"),
            (real, float, "Must be float"),
            (integer, str, "Must be string")
        )
        with pytest.raises(IllegalArgumentException):
            assert_types(all_at_once)

    @pytest.mark.parametrize('variable,type,message', [
        (integer, int, "Must be integer"),
        (real, float, "Must be float"),
        (word_string, str, "Must be string"),
        ([], list, "Must be list"),
        ((), tuple, "Must be tuple"),
        (object, object, "Must be generic object")
    ])
    def test_passing_valid_parameters(self, variable, type, message):
        assert_type(variable, type, message)
