""" Entry point. """

from stdout import (
    new_line, log, log_lines,
    error, warning, info,
    error_lines, warning_lines, info_lines
)
import conf
import flags

# Parse command line arguments.
flags.parse_arguments()

conf.print_conf(conf.max_log_lvl())


new_line()

