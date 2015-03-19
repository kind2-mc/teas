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

_log_lvl = 2
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





def print_conf(lvl):
    """ Prints the current state of the configuration module. """

    def print_conf_item(desc, val):
        """ Format prints a configuration item. """
        print( "  {:>29} | {}".format(desc, val) )

    if _log_lvl >= lvl:
        print("Configuration state:")
        print_conf_item("log level", log_lvl())
