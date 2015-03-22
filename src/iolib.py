""" Common io functions. """

import os

import flags
from excs import IOLibError

# File system io-s.

def norm_path(path):
    """ Retruns a normalized path. """
    return os.path.normpath(path)

def join_path(path1, path2):
    """ Returns the join two paths. """
    return os.path.join(path1, path2)

def abs_path(path):
    """ Returns the absolute path of a path. """
    return os.path.abspath(path)

def is_path_a_file(path):
    """ Checks if a path leads to an existing file. """
    if os.path.isfile(path): return True
    else: return False

def is_legal_dir_path(path, if_there_do=None, if_not_there_do=None):
    """ Checks a path. Fails if path leads to a file, or if its parent
    directory does not exist. Runs ``if_there_do`` if the path leads to an
    existing directory, and ``if_not_there_do`` if the path does not lead
    to a file but its parent is a directory. """
    if os.path.isfile(path): raise IOLibError(
        "\"{}\" is a file".format(path)
    )

    elif not os.path.isdir(path):
        split = os.path.split(path)
        if split[0] == "": parent = "./"
        else: parent = split[0]
        if not os.path.isdir(parent): raise IOLibError(
            "parent directory \"{}\" of \"{}\" does not exist".format(
                parent, path
            )
        )
        elif if_not_there_do != None: if_not_there_do()

    else:
        if if_there_do != None: if_there_do()

def mkdir(path):
    """ Creates a directory if necessary. Fails with ``IOLibError`` if path
    denotes a file, or path does does not exist and parent is not an existing
    directory. """
    try: is_legal_dir_path(
        path,
        if_not_there_do=(lambda: os.mkdir(path))
    )

    except IOLibError as e:
        raise IOLibError(
            "cannot mkdir, {}".format(e.args[0])
        )

    except OSError as e:
        raise IOLibError(
            "cannot mkdir, OSError ({}): {}".format(
                e.errno, e.strerror
            )
        )

    except IOError as e:
        raise IOLibError(
            "cannot mkdir, IOError ({}): {}".format(
                e.errno, e.strerror
            )
        )

