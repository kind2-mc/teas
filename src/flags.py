"""
Configuration module.

.. _conf_log:

=== 
Log 
===

The log level is an integer ranging between ``0`` and
``_max_log_lvl``. The log level is set when parsing the command
line arguments. The convention is

- ``0`` disables all output,
- ``1`` only enables errors and warnings,
- ``n`` enables all output where the log level specified is
  less than or equal to ``n``.

"""

# Log things.

_log_lvl_default = 2
_log_lvl = _log_lvl_default
_max_log_lvl = 3

def set_log_lvl(lvl):
    """ Sets the log level. """
    global _log_lvl, _max_log_lvl
    if lvl <= 0:
        _log_lvl = 0
    elif lvl >= _max_log_lvl:
        _log_lvl = _max_log_lvl
    else:
        _log_lvl = lvl

def log_lvl():
    """ Returns the log level. """
    return _log_lvl

def max_log_lvl():
    """ Returns the maximal log level. """
    return _max_log_lvl



# Test context things.

_type_check_test_cases_default = False
_type_check_test_cases = _type_check_test_cases_default

def type_check_test_cases():
    """ Returns true if the test cases should be type-checked. """
    return _type_check_test_cases

def set_type_check_test_cases(value):
    """ Sets the value of the test-case type check flag. """
    global _type_check_test_cases
    _type_check_test_cases = value

def type_check_test_cases_default():
    """ Returns the default value of the flag indicating if the
    test cases should be type-checked. """
    return _type_check_test_cases_default

# _test_context_format_default = "xml"
# _test_context_format_available = ["xml"]
# _test_context_format = _test_context_format_default

# def test_context_format():
#     """ Returns the format of the test context. """
#     return _test_context_format

# def set_test_context_format(value):
#     """ Sets the value of the test context format. """
#     global _test_context_format
#     _test_context_format = value

# def test_context_format_default():
#     """ Returns the default value of the format for test contexts. """
#     return _test_context_format_default

# def test_context_format_available():
#     """ Returns the available formats for test contexts. """
#     return _test_context_format_available


_flags = [
    ("log level", log_lvl()),
    ("Test context flags", None),
    ("type-check test cases", type_check_test_cases())
]


def print_flags(lvl):
    """ Prints the current state of the configuration module. """

    def print_conf_item(desc, val):
        """ Format prints a configuration item. """
        if val == None:
            print( "  {:<29} |".format("") )
            print( "| {:<29} |".format(desc) )
        else:
            print( "  {:>29} | {}".format(desc, val) )

    if log_lvl() >= lvl:
        print("Configuration state:")
        for flag in _flags:
            print_conf_item( flag[0], flag[1] )
