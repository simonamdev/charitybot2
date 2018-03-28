import functools

from charitybot2.exceptions import IllegalArgumentException


def assert_type(variable, variable_type, exception_message):
    try:
        assert isinstance(variable, variable_type)
    except AssertionError:
        raise IllegalArgumentException(exception_message)


def assert_types(variable_type_message_tuple):
    for variable, variable_type, exception_message in variable_type_message_tuple:
        assert_type(variable, variable_type, exception_message)


def accept_types(*required_types):
    # function has to be received, even if it is not used
    def accept_types_decorator(function):
        def wrapper(*args, **kwargs):
            types = required_types
            if not isinstance(required_types, tuple):
                types = list(required_types)
            # Zip matches up the types to the passed parameters
            matched_list = zip(types, args)
            for expected_type, given_argument in matched_list:
                assert_type(
                    given_argument,
                    expected_type,
                    'Value {} is not of expected type: {}'.format(given_argument, expected_type))
            return function(*args, **kwargs)
        return wrapper
    return accept_types_decorator
