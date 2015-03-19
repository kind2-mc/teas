""" Flag handling. """

import sys
from stdout import info, warning, error, new_line

# List of options. An option is a triplet of:
# * a list of string representations of the option,
# * a description of the option for help printing,
# * an action taking the tail of arguments and returning
#   its new state.
_options = []

def _print_help():
    """ Prints the options. """
    new_line()
    print("Options:")
    for triplet in _options:
        print( "  {}\n    {}".format(
            triplet[0], triplet[1]
        ) )
    new_line()

def _print_help_exit(code):
    """ Prints the options and exits. """
    _print_help()
    sys.exit(code)

# Help option.
_options.append(
    ( ["-h", "--help"],
      "prints the help message and exits",
      lambda tail: _print_help_exit(0) )
)

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
        if len(args) < 2:
            # One argument or less left, returning.
            return args
        else:
            option = args[0]
            triplet = _find_option_triplet(option)
            if triplet == None:
                # Unknown option, error.
                _print_help()
                error( "Unexpected option \"{}\".".format(option) )
                new_line()
                sys.exit(1)
            else:
                # Looping with updated tail of arguments.
                handle_options( triplet[2](args[1:]) )

    args = handle_options(args)

    info("Flags left: {}.".format(args))