""" Basic io operations. See conf_log_ for the semantics of the
log level. """

from conf import log_lvl

def new_line(lvl=2):
    """ Prints a new line. """
    log( "", lvl )

def log(line, lvl=2):
    """ Prints a line if `lvl` is greater than the log level. """
    if log_lvl() >= lvl:
        print("{}".format(line))

def log_lines(lines, lvl=2):
    """ Prints some lines if `lvl` is greater than the log level. """
    if log_lvl() >= lvl:
        for line in lines:
            print("{}".format(line))

# Prefixed single line printing.

def _error(line):
    """ Prints some line prefixed by `[ error ] `. """
    print( "[ error ] {}".format(line) )

def _warning(line):
    """ Prints some line prefixed by `[warning] `. """
    print( "[warning] {}".format(line) )

def _info(line):
    """ Prints some line prefixed by `[ info  ] `. """
    print( "[ info  ] {}".format(line) )

def error(line):
    """ Prints some line prefixed by `[ error ] `. """
    if log_lvl() >= 1: _error(line)

def warning(line):
    """ Prints some line prefixed by `[warning] `. """
    if log_lvl() >= 1: _warning(line)

def info(line, lvl=2):
    """ Prints some line prefixed by `[ info  ] `. """
    if log_lvl() >= lvl: _info(line)


# Prefixed multi line printing.

def error_lines(lines) :
    """ Prints some lines prefixed by `[ error ] `. """
    if log_lvl() >= 1:
        for line in lines : error(line)

def warning_lines(lines) :
    """ Prints some lines prefixed by `[warning] `. """
    if log_lvl() >= 1:
        for line in lines: _warning(line)


def info_lines(lines, lvl=2) :
    """ Prints some lines prefixed by `[ info  ] `. """
    if log_lvl() >= lvl:
        for line in lines: _info(line)