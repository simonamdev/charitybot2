from charitybot2.exceptions import IllegalArgumentException


def assert_type(variable, variable_type, exception_message):
    try:
        assert isinstance(variable, variable_type)
    except AssertionError:
        raise IllegalArgumentException(exception_message)


def assert_types(variable_type_message_tuple):
    for variable, variable_type, exception_message in variable_type_message_tuple:
        assert_type(variable, variable_type, exception_message)
