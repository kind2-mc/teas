""" Option handling. """

import sys

from stdout import log, warning, error, new_line
import flags

# List of options. An option is a triplet of:
# * a list of string representations of the option,
# * a description of the option for help printing,
# * an action taking the tail of arguments and returning its new
#   state.
#
# Additionally, an option with an empty list of representations
# is understood as an option section header.
_options = []

def _print_help():
    """ Prints the options. """
    print("")
    print("Usage: [options] <file>")
    for triplet in _options:
        if len(triplet[0]) < 1:
            new_line()
            for header_line in triplet[1]:
                print("|===| {}".format(header_line))
        else:
            print("> {}".format(triplet[0]))
            for desc_line in triplet[1]:
                print("  {}".format(desc_line))
    new_line()

def _print_help_exit(code):
    """ Prints the options and exits. """
    _print_help()
    sys.exit(code)

def _find_option_triplet(option):
    """ Finds the option triplet corresponding to an argument. """
    # Go through the list of options.
    for triplet in _options:
        # Return first match.
        if option in triplet[0]: return triplet

def parse_arguments():
    """ Parses the arguments and calls relevant actions. """

    # Ignore first package/file name argument.
    args = sys.argv[1:]

    def handle_options(args):
        """ Returns its input list if length of said list is one or
        less.
        Otherwise, finds the option triplet corresponding to
        the head of the list, applies the action, and loops on the
        resulting list. """
        if len(args) < 2:            # One argument or less left, returning.
            return args
        else:
            option = args[0]
            triplet = _find_option_triplet(option)
            if triplet == None:
                # Unknown option, error.
                _print_help()
                error( "Unexpected option \"{}\".".format(option) )
                new_line(1)
                sys.exit(1)
            else:
                try: nu_args = triplet[2](args[1:])
                except ValueError as e:
                    # Option handler crashed, error.
                    _print_help()
                    error( "Error on option \"{}\":".format(option) )
                    error( "  {}".format(e) )
                    new_line(1)
                    sys.exit(1)
                # Looping with updated tail of arguments.
                # Not tail call optimization T_T.
                else: return handle_options(nu_args)

    args = handle_options(args)

    return args








# Building the list of options.


def _add_option(reps, desc, l4mbda):
    """ Adds an option to the option list. """
    _options.append((reps, desc, l4mbda))

def _add_option_header(lines):
    """ Adds an option header to the option list. """
    _options.append((
        [],
        lines,
        "" # lambda tail: assert false
    ))

# Help option.
_add_option(
    ["-h", "--help"],
    ["prints the help message and exits"],
    lambda tail: _print_help_exit(0)
)

# Verbose option section header.
_add_option_header((
    ["Verbosity options."]
))

# Verbose option.
def _v_action(tail):
    flags.set_log_lvl(3)
    return tail
_add_option(
    ["-v"],
    ["verbose output"],
    _v_action
)

# Quiet 1 option.
def _q1_action(tail):
    flags.set_log_lvl(1)
    return tail
_add_option(
    ["-q"],
    ["no output except errors and warnings"],
    _q1_action
)

# Quiet 2 option.
def _q2_action(tail):
    flags.set_log_lvl(0)
    return tail
_add_option(
    ["-qq"],
    ["no output at all"],
    _q2_action
)

# Test case construction section header.
_add_option_header((
    ["Test context construction options."]
))

# Test case type-check option.
def _type_check_action(tail):
    if tail[0] in [ "true", "True" ]:
        flags.set_type_check_test_cases(True)
    elif tail[0] in [ "false", "False" ]:
        flags.set_type_check_test_cases(False)
    else: raise ValueError(
        "expected bool value but found \"{}\"".format(tail[0])
    )
    return tail[1:]
_add_option(
    ["--type_check"],
    [
        "> bool (default {})".format(
            flags.type_check_test_cases_default()
        ),
        "if true, test cases will be type checked (may be expensive",
        "for large test cases)"
    ],
    _type_check_action
)
