""" Entry point. """

import sys, os

from stdout import new_line, log, error, warning
import lib, options, flags, test_case, test_context, execution

max_log = flags.max_log_lvl()

# Parse command line arguments.
files = options.parse_arguments()

new_line()

flags.print_flags(max_log)
new_line(max_log)

new_line(max_log)
log( "Running on files {}.".format(files), max_log )
new_line(max_log)

test_contexts = []

for fil3 in files:
    log("Parsing test context from \"{}\".".format(fil3))
    context = test_context.of_file(fil3)
    log("Success.")
    new_line()
    test_context.print_test_context(context, max_log)
    new_line(max_log)

    for testcase in context["testcases"]:
        new_line(max_log)
        name = testcase["name"]
        path = testcase["file"]
        frmt = testcase["format"]
        log("Parsing test case \"{}\" from \"{}\" ({})".format(
            name, path, frmt
        ), max_log)
        input_seq = test_case.of_file(path)
        # Adding input sequence to the test case.
        testcase["inputs"] = input_seq
        test_case.print_test_case(input_seq, max_log)
        new_line(max_log)

    test_contexts.append(context)


# Break test contexts in test executions for parallel execution.
test_executions = []

for ctxt in test_contexts:

    fil3 = ctxt["file"]
    name = ctxt["name"]
    binaries = ctxt["binaries"]
    oracles = ctxt["oracles"]
    testcases = ctxt["testcases"]

    if len(binaries) < 1:
        warning("No binary in \"{}\" ({}), skipping it.".format(
            name, fil3
        ))
        new_line(1)
        continue

    if len(oracles) < 1:
        warning("No oracle in \"{}\" ({}), skipping it.".format(
            name, fil3
        ))
        new_line(1)
        continue

    if len(testcases) < 1:
        warning("No test case in \"{}\" ({}), skipping it.".format(
            name, fil3
        ))
        new_line(1)
        continue

    # Context file directory.
    context_dir = lib.file_name_of_path(fil3)
    if os.path.isdir(context_dir):
        warning("Log directory    \"{}\"".format(context_dir))
        warning("for context file \"{}\" already exists.".format(fil3))
        new_line(1)
    else:
        log("Creating log directory \"{}\"".format(context_dir),
            max_log)
        log("for context file       \"{}\".".format(fil3),
            max_log)
        new_line(max_log)
        # os.makedirs(os.path.join(context_dir))


    for binary in binaries:

        binary_name = binary["name"]

        # Binary subdirectory.
        binary_dir = os.path.join(
            context_dir, lib.to_file_name(binary_name)
        )
        if os.path.isdir(binary_dir):
            warning("Log directory \"{}\"".format(binary_dir))
            warning("for binary    \"{}\" already exists.".format(
                binary_name
            ))
            new_line(1)
        else:
            log("Creating log directory \"{}\"".format(binary_dir),
                max_log)
            log("for binary             \"{}\".".format(binary_name),
                max_log)
            new_line(max_log)
            # os.makedirs(os.path.join(binary_dir))

        for testcase in testcases:

            testcase_file = testcase["file"]

            # Binary subdirectory.
            testcase_log_file = "{}.res".format(os.path.join(
                binary_dir, lib.file_name_of_path(testcase_file)
            ))
            if os.path.isfile(testcase_log_file):
                warning("Log file     \"{}\"".format(testcase_log_file))
                warning("for testcase \"{}\" already exists.".format(
                    testcase_file
                ))
                new_line(1)

            log("Launching \"{}\" on test case \"{}\".".format(
                binary["name"], testcase["name"]
            ))
            log("Logging to \"{}\".".format(testcase_log_file),
                max_log)
            new_line(max_log)

            execution.run_binary(execution.mk_test_execution(
                name, testcase_log_file, binary, testcase, oracles
            ))


new_line()
log("Done.")
new_line()
