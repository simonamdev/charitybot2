import pytest
from charitybot2.exceptions import IllegalArgumentException
from type_assertions import assert_types, assert_type, accept_types

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

    def test_wrapping_function_with_type_assertion(self):
        @accept_types(str)
        def wrap_test(this_should_be_string):
            pass
        wrap_test('bla')

    def test_wrapping_function_returns_function_if_types_are_correct(self):
        @accept_types(int)
        def multiply_by_5(number):
            return number * 5
        assert 25 == multiply_by_5(5)

    def test_receiving_incorrect_expected_type_throws_exception(self):
        @accept_types(str, int)
        def two_strings(one, two):
            pass
        with pytest.raises(IllegalArgumentException):
            two_strings('Actually a string', 'Also a string')

    def test_receiving_custom_object_types(self):
        class Foo:
            pass

        class Bar:
            pass

        @accept_types(Foo, Bar)
        def do_re_mi(something_that_is_foo, something_that_is_bar):
            pass
        do_re_mi(Foo(), Bar())

    def test_receiving_keyword_arguments(self):
        @accept_types(int, float)
        def add_one(rounded_number=3, decimal_number=5.0):
            print(decimal_number)
            return rounded_number + 1
        assert 4 == add_one(decimal_number=3.333)
        assert 4 == add_one(rounded_number=3)
        assert 4 == add_one(rounded_number=3, decimal_number=1.1)
        assert 4 == add_one(decimal_number=3.3, rounded_number=3)

    def test_receiving_incomplete_arguments_due_to_defaults(self):
        @accept_types(str, int)
        def return_one_if_none(message, timestamp=None):
            if timestamp is None:
                return 1
            return timestamp
        assert 1 == return_one_if_none('foo')
        assert 1 == return_one_if_none('foo', 1)
        assert 5 == return_one_if_none('foo', 5)

    def test_passing_same_as_default_throws_exception(self):
        @accept_types(str, int)
        def return_two_if_none(message, timestamp=None):
            if timestamp is None:
                return 2
            return timestamp
        with pytest.raises(IllegalArgumentException):
            return_two_if_none('bar', None)
