""" Test execution. Runs one test case on some binary.
A test execution is a name (of the context), a log file,
a binary, a testcase and some oracles. """

import os, subprocess

import lib, test_case, flags
from stdout import log, warning, error

max_log = flags.max_log_lvl()

def mk_test_execution(
    name, fil3, log_file, binary, testcase, oracles
):
    """ Builds a test execution dictionnary. """
    return {
        "name": name,
        "file": fil3,
        "log_file": log_file,
        "binary": binary,
        "testcase": testcase,
        "oracles": oracles
    }

def print_test_execution(test_execution, lvl=2, print_test_case=False):
    """ Prints a test execution. """
    log("> log_file | {}".format(test_execution["log_file"]), lvl)
    log("> binary   | {}".format(test_execution["binary"]["name"]), lvl)
    log("> testcase | {}".format(test_execution["testcase"]["name"]), lvl)
    oracles = test_execution["oracles"]
    log("> oracles  | {}".format(oracles[0]["name"]), lvl)
    if len(oracles) > 1:
        for oracle in oracles[1:]:
            log("           | {}".format(oracle["name"]), lvl)
    if print_test_case:
        test_case.print_test_case(
            test_execution["testcase"]["inputs"],
            lvl
        )

def write_out_file_header(fil3, test_execution):
    """ Writes the header of a test execution to a file.
    Writes the path to the original xml test context file, to the binary being
    tested, to the test case cvs file, and to the oracles used. """
    def w(s): fil3.write(s)

    binary = test_execution["binary"]
    testcase = test_execution["testcase"]

    w(  (
            "# Result file for test execution\n"
            "# > as specified in | {}\n"
            "# > for binary      | {} ({})\n"
            "# > for testcase    | {} ({})\n"
            "# > with oracles\n"
        ).format(
            test_execution["file"],
            binary["name"], lib.string_join(binary["cmd"]),
            testcase["name"], testcase["file"]
        )
    )

    for oracle in test_execution["oracles"]:
        if oracle["global"]: glb = "[global]"
        else: glb = "[      ]"
        w( (
            "#   > {} {} ({})\n"
        ).format(
            glb,
            oracle["name"],
            lib.string_join(oracle["cmd"], " ")
        ) )

    w( "\n" )

def run(test_execution):
    """ Runs a test_case for some binary. Result is logged as a csv file. """

    file_name = test_execution["log_file"]
    binary = test_execution["binary"]
    testcase = test_execution["testcase"]
    fil3 = None
    proc3ss = None

    try:
        # Open out file in write mode.
        fil3 = open( file_name, "w" )

        # Write test execution header.
        write_out_file_header(fil3, test_execution)

        # # Start subprocess with pipe on stdin, stdout and stderr.
        # proc3ss = subprocess.Popen(
        #     binary["cmd"],
        #     stdin=PIPE,
        #     stdout=PIPE,
        #     stderr=PIPE
        # )

        test_case.to_file(testcase, None, False)

    # Whatever happens, close the file if it's still open.
    finally:
        if fil3 != None: fil3.close()
