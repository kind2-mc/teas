""" Basic helper things. """

import os, string

def bool_of_string(string):
    """ Parses a boolean, raises ValueError. """
    if string in [ "true", "True" ]: return True
    elif string in [ "false", "False"]: return False
    else: raise ValueError(
        "expected bool but found \"{}\"".format(string)
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


def to_file_name(s):
    """ Replaces whitespaces by underscores. """
    return string.join(string.split(s), "_")