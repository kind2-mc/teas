""" Entry point. """

from stdout import ( new_line, log )
import options
import flags
import test_case
import test_context

max_log = flags.max_log_lvl()

# Parse command line arguments.
files = options.parse_arguments()

new_line()

flags.print_flags(max_log)
new_line(max_log)

new_line(max_log)
log( "Running on files {}.".format(files), max_log )
new_line(max_log)

for fil3 in files:
    log("Parsing test context from \"{}\".".format(fil3))
    context = test_context.of_file(fil3)
    log("Success.")
    test_context.print_test_context(context, max_log)
    new_line(max_log)

    for testcase in context[2]:
        new_line(max_log)
        path = testcase[0]
        name = testcase[1]
        frmt = testcase[2]
        log("Parsing test case \"{}\" from \"{}\" ({})".format(
            name, path, frmt
        ), max_log)
        testcase = test_case.of_file(path)
        test_case.print_test_case(testcase, max_log)

new_line()
log("Done.")
new_line()

