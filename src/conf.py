""" Configuration module. """

class _Log:
    lvl = 4

def set_log_lvl(lvl):
    """ Sets the log level. """
    if   lvl <= 0: _Log.lvl = 0
    elif lvl >= 4: _Log.lvl = 4
    else:          _Log.lvl = lvl

def log_lvl():
    """ The log level. """
    return _Log.lvl