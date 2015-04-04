""" Basic helper things. """

import os, string

def bool_of_string(s):
    """ Converts a string to a bool, raises a ``ValueError`` in case of
    failure. """
    if s in [ "t", "T", "true", "True" ]: return True
    elif s in [ "f", "F", "false", "False"]: return False
    else: raise ValueError(
        "expected bool but found \"{}\"".format(s)
    )

def int_of_string(s):
    """ Converts a string to an int, raises a ``ValueError`` in case of
    failure. """
    try: return int(s)
    except ValueError: raise ValueError(
        "Expected integer but found \"{}\"".format(s)
    )

def file_name_of_path(path):
    """ Returns the file name, whithout the extension if any,
    from a path. """
    split = os.path.split(path)
    split = string.split(split[1], ".")
    if len(split) <= 2:
        return split[0]
    else:
        split.pop()
        return string.join(split, ".")

def string_join(s, sep=" "):
    """ Joins a list of strings. """
    return string.join(s, sep)

def to_file_name(s):
    """ Replaces whitespaces by underscores. """
    return string_join(string.split(s), "_")

def oracle_log_file_of_log_path(log_path):
    """ Returns a log file for an oracle output from the log path of a test
    execution. """
    if log_path.endswith(".csv"): clean_path = log_path[:-4]
    else: clean_path = log_path
    return "{}_{}.csv".format(
        clean_path, "oracles"
    )