""" Entry point. """

from stdout import (
    new_line, log, log_lines,
    error, warning, info,
    error_lines, warning_lines, info_lines
)
import conf
import flags
import input_seq

# Parse command line arguments.
flags.parse_arguments()

conf.print_conf(conf.max_log_lvl())

test_csv_file = "resources/test1.csv"

new_line()

log("Attempting to read \"{}\".".format(test_csv_file))

test_case = input_seq.of_csv_file(test_csv_file)

log("Success:")

input_seq.print_test_case(test_case, 2)


new_line()

