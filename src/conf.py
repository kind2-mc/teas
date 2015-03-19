""" Configuration module. """

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





def print_conf():
    """ Prints the current state of the configuration module. """

    def print_conf_item(desc, val):
        """ Format prints a configuration item. """
        print( "  {:>29} | {}".format(desc, val) )

    print("Configuration state:")
    print_conf_item("log level", log_lvl())
