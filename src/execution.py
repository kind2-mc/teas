""" Test execution. Runs one test case on some binary.
A test execution is a name (of the context), a log file,
a binary, a testcase and some oracles. """

import os

import lib, test_case, flags
from stdout import new_line, log, warning, error

max_log = flags.max_log_lvl()

def mk_test_execution(
    name, log_file, binary, testcase, oracles
):
    """ Builds a test execution dictionnary. """
    return {
        "name": name,
        "log_file": log_file,
        "binary": binary,
        "testcase": testcase,
        "oracles": oracles
    }

def run_binary(test_execution):
    """ Runs a test_case for some binary.
    Result is logged as a csv file. """

    log("Running {}".format(test_execution["name"]))
    log("> log_file | {}".format(test_execution["log_file"]))
    log("> binary   | {}".format(test_execution["binary"]["name"]))
    log("> testcase | {}".format(test_execution["testcase"]["name"]))
    oracles = test_execution["oracles"]
    log("> oracles  | {}".format(oracles[0]["name"]))
    if len(oracles) > 1:
        for oracle in oracles[1:]:
            log("           | {}".format(oracle["name"]))

    new_line()
    test_case.print_test_case(
        test_execution["testcase"]["inputs"],
        max_log
    )
    new_line(max_log)

