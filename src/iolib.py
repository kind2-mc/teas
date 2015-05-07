""" Common io functions. """

import shlex
import os, sys

import flags
from excs import IOLibError
from stdout import log, new_line

# File system io-s.

def norm_path(path):
    """ Returns a normalized path. """
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

# Process io-s.

def split_cmd(cmd):
    """Splits a command in a list of strings."""
    split = shlex.split(cmd)
    split[0] = norm_path(split[0])
    return split

def input_sequences_to_file(
    inputs, length, fil3, close_when_done=True
):
    """ Prints the input sequences as comma separated values between parens,
    separated by newlines. Closes the file when done if the flag says to do
    so. """
    index = 0
    def w(s): log(s, flags.max_log_lvl())
    while index < length:
        w( "({}".format(inputs[0]["seq"][index]) )
        for inpuT in inputs[1:]:
            w( ", {}".format(inpuT["seq"][index]) )
        # In theory, python will translate the newline for windows.
        w( ")\n" )
        index += 1
    if close_when_done: fil3.close()

def file_to_output_sequences(
    outputs, length, fil3, close_when_done=True, data=None
):
    """ Reads the output sequences as comma separated values between parens,
    separated by newlines. Returns when enough tuples of values specified
    by ``output_sequence`` have been read.
    Closes the file when done if the flag says to do so. """
    tuple_count = 0
    def update(tuple):
        index = 0
        while index < len(tuple):
            outputs[index]["seq"].append(tuple[index])
            index += 1
    def update_of_string(s):
        update(s.replace("(","").split(","))
    data.reverse()
    def r(): return data.pop()
    out = ""
    while tuple_count < length:
        out = out + r()
        temp = "".join(out.split()).split(")")
        # Temp cannot be empty, this is safe.
        out = temp.pop()
        map( update_of_string, temp )
        tuple_count += len(temp)
    if close_when_done: fil3.close()

# Parsing stuff.

def bool_of_str(s):
    """Converts a string to a boolean."""
    if s in ["true","True"]:
        return True
    elif s in ["false","False"]:
        return False
    else: raise TypeError(
        "expected boolean but found \"{}\"".format(s)
    )


