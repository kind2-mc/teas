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


# Test execution things.

_run_tests_default = True
_run_tests = _run_tests_default

def run_tests():
    """ Returns true if the tests should be ran. """
    return _run_tests

def set_run_tests(value):
    """ Sets the value of the run_tests flag. """
    global _run_tests
    _run_tests = value

def run_tests_default():
    """ Returns the default value of the run_tests flag. """
    return _run_tests_default

_max_proc_default = 4
_max_proc = _max_proc_default

def max_proc():
    """ Returns the maximum number of processes to run in
    parallel. """
    return _max_proc

def set_max_proc(value):
    """ Sets the value of the max_proc flag. """
    global _max_proc
    _max_proc = value

def max_proc_default():
    """ Returns the default value of the max_proc flag. """
    return _max_proc_default

_out_dir_default = "./"
_out_dir = _out_dir_default

def out_dir():
    """ Returns the out directory. """
    return _out_dir

def set_out_dir(value):
    """ Sets the value of the out directory. """
    global _out_dir
    _out_dir = value

def out_dir_default():
    """ Returns the default value for the out directory. """
    return _out_dir_default




_flags = [
    ("log level", log_lvl),
    ("Test context flags", None),
    ("type-check test cases", type_check_test_cases),
    ("Test execution flags", None),
    ("run tests", run_tests),
    ("max proc count", max_proc),
    ("out directory", out_dir),
]


def print_flags(lvl):
    """ Prints the current state of the configuration module. """

    def print_conf_item(desc, val_fun):
        """ Format prints a configuration item. """
        if val_fun == None:
            print( "  {:<29} |".format("") )
            print( "| {:<29} |".format(desc) )
        else:
            print( "  {:>29} | {}".format(desc, val_fun()) )

    if log_lvl() >= lvl:
        print("Configuration state:")
        for flag in _flags:
            print_conf_item( flag[0], flag[1] )
