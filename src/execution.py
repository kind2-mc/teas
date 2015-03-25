""" Test execution. Runs one test case on some binary.
A test execution is a name (of the context), a log file,
a binary, a testcase and some oracles. """

import os, subprocess, random

import lib, test_case, flags, iolib, outcome
from stdout import log, warning, error, new_line

max_log = flags.max_log_lvl()

def mk_test_execution(
    name, fil3, log_file, breakdown_file, binary, testcase, oracles
):
    """ Builds a test execution dictionnary. """
    return {
        "name": name,
        "file": fil3,
        "log_file": log_file,
        "breakdown_file": breakdown_file,
        "binary": binary,
        "testcase": testcase,
        "oracles": oracles
    }

def print_test_execution(test_execution, lvl=2, print_test_case=False):
    """ Prints a test execution. """
    log("> log_file  | {}".format(test_execution["log_file"]), lvl)
    log("> breakdown | {}".format(test_execution["breakdown_file"]), lvl)
    log("> binary    | {}".format(test_execution["binary"]["name"]), lvl)
    log("> testcase  | {}".format(test_execution["testcase"]["name"]), lvl)
    oracles = test_execution["oracles"]
    log("> oracles   | {}".format(oracles[0]["name"]), lvl)
    if len(oracles) > 1:
        for oracle in oracles[1:]:
            log("            | {}".format(oracle["name"]), lvl)
    if print_test_case:
        test_case.print_test_case(
            test_execution["testcase"]["inputs"],
            lvl
        )

def write_out_file_header(fil3, test_execution, title="test execution"):
    """ Writes the header of a test execution to a file.
    Writes the path to the original xml test context file, to the binary being
    tested, to the test case cvs file, and to the oracles used. """
    def w(s): fil3.write(s)

    binary = test_execution["binary"]
    testcase = test_execution["testcase"]

    w(  (
            "# Result file for {}\n"
            "# > as specified in | {}\n"
            "# > for binary      | {} ({})\n"
            "# > for testcase    | {} ({})\n"
            "# > with oracles\n"
        ).format(
            title,
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

    w( "# \n" )

def run(test_execution):
    """ Runs a test_case for some binary. Result is logged as a csv file. """

    file_name = test_execution["log_file"]
    binary = test_execution["binary"]
    testcase = test_execution["testcase"]
    oracles = test_execution["oracles"]
    length = testcase["length"]
    fil3 = None
    oracle_fil3 = None
    binary_proc3ss = None
    oracle_proc3sses = []

    try:

        # # Start subprocess with pipe on stdin, stdout and stderr.
        # proc3ss = subprocess.Popen(
        #     binary["cmd"],
        #     stdin=PIPE,
        #     stdout=PIPE,
        #     stderr=PIPE
        # )

        log("Printing input sequence to binary stdin.", max_log)
        iolib.input_sequences_to_file(
            testcase["inputs"], length, None, False
        )
        new_line(max_log)

        # Dummy output sequences.
        testcase["outputs"] = [
            { "ident": "out1", "type": "int", "seq": [] },
            { "ident": "out2", "type": "float", "seq": [] }
        ]

        if length == 6:
            data = [
                "(0, 0.) (7, .69)",
                "(3, 3.) (42",
                ", 17.7) (1, ",
                "1.) (0, 0.1)"
            ]
        else: data = [
            "(0, 0.) (7, .69)",
            "(3, 3.) (42",
            ", 17.7) (1, ",
            "1.) (0, 0.1)",
            "(2, 0.3) (6,",
            "0.1)",
        ]

        iolib.file_to_output_sequences(
            testcase["outputs"], length, None, False, data
        )

        # Open out file in write mode.
        fil3 = open( file_name, "w" )
        # Write test execution header.
        write_out_file_header(fil3, test_execution)

        log("output sequence ({}):".format(length), max_log)
        for output in testcase["outputs"]:
            log("> {:10}: {:10} | {}".format(
                output["ident"], output["type"], output["seq"]
            ), max_log)
            fil3.write("{},{}".format(
                output["ident"],output["type"]
            ))
            for val in output["seq"]:
                fil3.write(",{}".format(val))
            fil3.write("\n")
        new_line(max_log)

        # Oracle sequence is the join of the input and the output sequence.
        oracle_inputs = []
        for input_seq in testcase["inputs"]:
            oracle_inputs.append(input_seq)
        for output_seq in testcase["outputs"]:
            oracle_inputs.append(output_seq)
        testcase["oracle_inputs"] = oracle_inputs

        log("oracle input sequence ({}):".format(length), max_log)
        for inp in testcase["oracle_inputs"]:
            log("> {:10}: {:10} | {}".format(
                inp["ident"], inp["type"], inp["seq"]
            ), max_log)
        new_line(max_log)

        # Start oracle subprocesses with pipe on stdin, stdout and stderr.
        oracle_outputs = []
        for oracle in oracles:
            proc = None
            oracle_outputs.append(
                {
                    "oracle": oracle,
                    "seq": [],
                    "proc": proc,
                }
            )
            oracle_proc3sses.append(proc)

        def get_bool():
            return "({})".format(random.randint(0,1) == 1)

        for oracle in oracle_outputs:
            data = map(
                ( lambda i: get_bool() ),
                range(length)
            )
            iolib.file_to_output_sequences(
                [ oracle ],
                length,
                oracle["proc"],
                False,
                data
            )
        testcase["oracle_outputs"] = oracle_outputs

        # Open oracle output file in write mode.
        oracle_file_name = lib.oracle_log_file_of_log_path(file_name)
        oracle_fil3 = open(
            oracle_file_name,
            "w"
        )
        # Write test execution header.
        write_out_file_header(oracle_fil3, test_execution, "oracle outputs")

        log("oracle_outputs ({}):".format(length), max_log)
        for oracle_out in testcase["oracle_outputs"]:
            oracle = oracle_out["oracle"]
            log("  {:10} | {}".format(
                oracle["name"],
                oracle_out["seq"]
            ), max_log)
            oracle_fil3.write(
                "# {} ({})".format( oracle["name"], oracle["cmd"] )
            )
            if oracle["global"]: 
                oracle_fil3.write( " (global)" )
            oracle_fil3.write( "\n" )
            oracle_fil3.write( oracle_out["seq"][0] )
            for val in oracle_out["seq"][1:]:
                oracle_fil3.write( ",{}".format(val) )
            oracle_fil3.write( "\n" )
        new_line(max_log)

        outcome.generate_breakdown_and_outcome(test_execution)



    # Whatever happens, close the file if it's still open.
    finally:
        if fil3 != None: fil3.close()
        if oracle_fil3 != None: oracle_fil3.close()
        if binary_proc3ss != None: binary_proc3ss.close()
        for proc in oracle_proc3sses:
            if proc != None: proc.close()
