""" Option handling. """

import sys, os

from stdout import log, warning, error, new_line
import flags, lib, iolib

# List of options. An option is a triplet of:
# * a list of string representations of the option,
# * a description of the option for help printing,
# * an action taking the tail of arguments and returning its new
#   state.
#
# Additionally, an option with an empty list of representations
# is understood as an option section header.
_options = []

_options_end = "--"

def _print_help():
    """ Prints the options. """
    log("", 1)
    log("Usage: <option>* <file>", 1)
    log("   or: <option>* {} <file>+".format(_options_end), 1)
    log("where <option> can be", 1)
    for triplet in _options:
        if len(triplet[0]) < 1:
            new_line(1)
            for header_line in triplet[1]:
                log("|===| {}".format(header_line), 1)
        else:
            log("> {}".format(triplet[0]), 1)
            for desc_line in triplet[1]:
                log("  {}".format(desc_line), 1)
    new_line(1)

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

_help_flags = ["-h", "--help"]

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
        if len(args) < 2:
            # One argument or less left, returning.
            return args
        else:
            option = args[0]
            triplet = _find_option_triplet(option)
            if option == _options_end:
                # End of option, remaining arguments should be files.
                return args[1:]
            elif triplet == None:
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
                    error( "> {}.".format(e) )
                    new_line(1)
                    sys.exit(1)
                # Looping with updated tail of arguments.
                # Not tail call optimization T_T.
                else: return handle_options(nu_args)

    if len(args) < 1:
        _print_help()
        error("No file specified.")
        new_line(1)
        sys.exit(1)

    for f in _help_flags:
        if f in args:
            _print_help()
            new_line(1)
            sys.exit(0)

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
    _help_flags,
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

# Adding binaries option.
def _add_binary_action(tail):
    if len(tail) < 3: raise ValueError(
        "expected three arguments but found {}".format(len(tail))
    )
    fst = tail[0]
    snd = tail[1]
    thd = tail[2]
    triple = fst, snd, thd
    if fst.startswith("-"): raise ValueError(
        "expected binary name but found \"{}\"".format(fst)
    )
    if snd.startswith("-"): raise ValueError(
        "expected binary command but found \"{}\"".format(snd)
    )
    if thd.startswith("-"): raise ValueError(
        "expected test context file but found \"{}\"".format(thd)
    )
    if not os.path.isfile(thd): raise ValueError(
        "test context file \"{}\" does not exist".format(thd)
    )
    flags.add_binary_to_add(triple)
    return tail[3:]
_add_option(
    ["--add_bin"],
    [
        "> of n cmd ctxt (default {})".format(
            flags.binaries_to_add_default()
        ),
        "will add the binary with name \"n\", command \"cmd\" to the test",
        "context in file \"ctxt\""
    ],
    _add_binary_action
)

# Test case type-check option.
def _type_check_action(tail):
    flags.set_type_check_test_cases( lib.bool_of_string(tail[0]) )
    return tail[1:]
_add_option(
    ["--type_check"],
    [
        "> of bool (default {})".format(
            flags.type_check_test_cases_default()
        ),
        "if true, test cases will be type checked (may be expensive",
        "for large test cases)"
    ],
    _type_check_action
)


# Test execution section header.
_add_option_header((
    ["Test execution options."]
))

# Run tests option.
def _run_tests_action(tail):
    flags.set_run_tests( lib.bool_of_string(tail[0]) )
    return tail[1:]
_add_option(
    ["--run_tests"],
    [
        "> bool (default {})".format(
            flags.run_tests_default()
        ),
        "if true, test cases will be executed"
    ],
    _run_tests_action
)

# Max proc option.
def _max_proc_action(tail):
    flags.set_max_proc( lib.int_of_string(tail[0]) )
    return tail[1:]
_add_option(
    ["--max_proc"],
    [
        "> int (default {})".format(
            flags.max_proc_default()
        ),
        "maximum number of processes to run in parallel"
    ],
    _max_proc_action
)


# Output directory option.
def _out_dir_action(tail):
    path = tail[0]
    iolib.is_legal_dir_path(
        path,
        if_not_there_do=(lambda: warning(
            ("Output directory \"{}\" does not exist "
             "and will be created.\n").format(path)
        ))
    )
    flags.set_out_dir(path)
    return tail[1:]
_add_option(
    ["--out_dir"],
    [
        "> path (default {})".format(
            flags.out_dir_default()
        ),
        "sets the output directory"
    ],
    _out_dir_action
)
