"""Entry point."""

from stdout import (
    new_line, log, log_lines,
    error, warning, info,
    error_lines, warning_lines, info_lines
)
import conf
import flags

new_line()

flags.parse_arguments()



new_line()