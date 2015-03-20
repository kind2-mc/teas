""" Entry point. """

from stdout import (
    new_line, log, log_lines,
    error, warning, info,
    error_lines, warning_lines, info_lines
)
import options
import flags
import test_case
import test_context

# Parse command line arguments.
files = options.parse_arguments()

new_line()
log( "Running on files {}.".format(files) )
new_line()

flags.print_flags(flags.max_log_lvl())
new_line(flags.max_log_lvl())

for fil3 in files:
    log("Building test context from \"{}\".".format(fil3))

    context = test_context.of_xml(fil3)
    log("Success:")
    test_context.print_test_context(context)
    new_line()

new_line()
log("Done.")
new_line()

