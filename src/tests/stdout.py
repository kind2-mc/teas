""" Tests log related things. """

from src.conf import set_log_lvl
from src.stdout import (
    new_line, log, log_lines,
    error, warning, info,
    error_lines, warning_lines, info_lines
)

def _test_log(lvl):
    set_log_lvl(lvl)

    log("testing log default")
    new_line()
    log("testing log 0", 0)
    new_line(0)
    log("testing log 1", 1)
    new_line(1)
    log("testing log 2", 2)
    new_line(2)
    log("testing log 3", 3)
    new_line(3)

    error("testing error")
    warning("testing warning")
    info("testing info default")
    info("testing info 0", 0)
    info("testing info 1", 1)
    info("testing info 2", 2)
    info("testing info 3", 3)

    error_lines(["testing", "error", "lines"])
    warning_lines(["testing", "warning", "lines"])
    info_lines(["testing", "info", "lines"])


def test_log_0():
    """ Test log functions for a log level of 0 """
    _test_log(0)

def test_log_1():
    """ Test log functions for a log level of 1 """
    _test_log(1)

def test_log_2():
    """ Test log functions for a log level of 2 """
    _test_log(2)

def test_log_3():
    """ Test log functions for a log level of 3 """
    _test_log(3)