""" Entry point. """

import sys, os

from stdout import new_line, log, error, warning
import lib, iolib, options, flags, test_case, test_context, execution

max_log = flags.max_log_lvl()

new_line(1)

# Parse command line arguments.
all_files = options.parse_arguments()

# Print configuration.
flags.print_flags(max_log)
new_line(max_log)

# Only keeping files that actually exist.
def file_exists(path):
    if iolib.is_path_a_file(path): return True
    else:
        warning("Skipping input file \"{}\" (does not exist).".format(path))
        warning("")
        return False
files = filter( file_exists, all_files )

# Exiting if no file to run on.
if len(files) < 1:
    warning("No file to run on, done.")
    warning("")
    sys.exit(0)

# Create output directory if necessary.
try: iolib.mkdir(flags.out_dir())
except iolib.IOLibError as e:
    error("while creating output directory:")
    error("> {}".format(e.msg))
    error("")
    sys.exit(1)

# Starting to do things.
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
    context_dir = iolib.join_path(
        flags.out_dir(), lib.file_name_of_path(fil3)
    )
    if os.path.isdir(context_dir):
        warning("Log directory    \"{}\"".format(context_dir))
        warning("for context file \"{}\"".format(fil3))
        warning("already exists.")
        new_line(1)
    else:
        log("Creating log directory \"{}\"".format(context_dir),
            max_log)
        log("for context file       \"{}\".".format(fil3),
            max_log)
        new_line(max_log)
        try: iolib.mkdir(context_dir)
        except iolib.IOLibError as e:
            error("{}".format(e.msg))
            new_line(1)
            continue


    for binary in binaries:

        binary_name = binary["name"]

        # Binary subdirectory.
        binary_dir = os.path.join(
            context_dir, lib.to_file_name(binary_name)
        )
        if os.path.isdir(binary_dir):
            warning("Log directory \"{}\"".format(binary_dir))
            warning("for binary    \"{}\"".format(
                binary_name
            ))
            warning("already exists.")
            new_line(1)
        else:
            log("Creating log directory \"{}\"".format(binary_dir),
                max_log)
            log("for binary             \"{}\".".format(binary_name),
                max_log)
            new_line(max_log)
            try: iolib.mkdir(binary_dir)
            except iolib.IOLibError as e:
                error("{}".format(e.msg))
                new_line(1)
                continue

        for testcase in testcases:

            testcase_file = testcase["file"]

            # Binary subdirectory.
            testcase_log_file = "{}.res".format(os.path.join(
                binary_dir, lib.file_name_of_path(testcase_file)
            ))
            if os.path.isfile(testcase_log_file):
                warning("Log file     \"{}\"".format(testcase_log_file))
                warning("for testcase \"{}\"".format(
                    testcase_file
                ))
                warning("already exists.")
                new_line(1)

            log("Launching \"{}\" on test case \"{}\".".format(
                binary["name"], testcase["name"]
            ))
            log("Logging to \"{}\".".format(testcase_log_file),
                max_log)
            new_line()

            test_execution = execution.mk_test_execution(
                name, fil3, testcase_log_file, binary, testcase, oracles
            )
            execution.print_test_execution(
                test_execution, max_log, True
            )

            execution.run(test_execution)


new_line()
log("Done.")
new_line(1)
