""" The outcome of a test execution is either ``Success`` or ``Failure``. """

import lib, iolib
from stdout import log

def get_file_path(root_path, binary_name, testcase_file):
    clean_bin_name = lib.to_file_name(binary_name)
    clean_testcase_name = lib.file_name_of_path(testcase_file)
    return iolib.join_path(root_path, "{}.{}.md".format(
        clean_bin_name, clean_testcase_name
    ))

def first_failure_of_oracles(oracle_outputs, length):
    """ Inspects a list of oracle for a failure.
    A failure occurs when either

    - a global oracle output is false, or
    - no non-global oracle output is true.

    Output is a sequence and contains

    - nothing if no failure was detected,
    - an index and a list of global oracles which output is false at that
      index,
    - only an index if the failure comes from all non-global oracles
      evaluating to false."""
    global_oracles = []
    mode_oracles = []
    for oracle_output in oracle_outputs:
        oracle = oracle_output["oracle"]
        if oracle["global"]: global_oracles.append(oracle_output)
        else: mode_oracles.append(oracle)

    index = 0
    result = []
    def log_orcl(o,i):
        log("{}[{}]: {}".format(o["oracle"]["name"], i, o["seq"][i]))
        return "False" == o["seq"][i]
    while index < length:
        result = filter(
            (lambda o: not lib.bool_of_string(o["seq"][index])),
            global_oracles
        )
        if len(result) != 0: break
        mode_disj = reduce(
            (lambda disj, o: disj or o["seq"][index]),
            mode_oracles,
            True
        )
        if not mode_disj: break
        index += 1

    if index < length: return [
        index, map( (lambda o: o["oracle"]), result )
    ]
    return []

def generate_breakdown_and_outcome(testex_result):
    testcase = testex_result["testcase"]
    length = testcase["length"]
    inputs = testcase["inputs"]
    outputs = testcase["outputs"]
    oracles = testex_result["oracles"]
    binary_name = testex_result["binary"]["name"]
    binary_cmd = lib.string_join(testex_result["binary"]["cmd"])
    binary_desc = testex_result["binary"]["desc"]
    context_file = testex_result["file"]
    oracle_outputs = testcase["oracle_outputs"]

    brkdwn_file = None

    try:
        brkdwn_file = open(testex_result["breakdown_file"], "w")

        # Success => []
        # Global failure => [index, global_oracles_falsified_seq]
        # Mode failure => [index]
        first_failure_seq = first_failure_of_oracles(oracle_outputs, length)
        success = len(first_failure_seq) == 0

        def w(s): brkdwn_file.write(s)

        w("# Run for \"{}\" on {}\n\n".format(
            binary_name, testcase["file"]
        ))

        failure_index = -1
        failed_oracles = []

        if success:
            w("## Success\n\n")
        else:
            failure_index = first_failure_seq[0]
            failed_oracles = first_failure_seq[1]
            w("## Failure\n\n")
            if len(failed_oracles) == 0:
                w(
                    ("No non-global oracle evaluates to true "
                     "at step {}.\n\n").format(
                        failure_index
                    )
                )
            elif len(failed_oracles) == 1:
                w(
                    ("Global oracle evaluates to false "
                     "at step {}:\n\n").format(
                        failure_index
                    )
                )
            else:
                w(
                    ("Some global oracles evaluate to false "
                     "at step {}:\n\n.").format(
                        failure_index
                    )
                )
            for oracle in failed_oracles:
                w("  * {}\n".format(oracle["name"]))
                for line in oracle["desc"]: w("    {}\n".format(line))
                w("\n")
            w("\n")

        w("|")
        for i in inputs:
            w(" {} |".format(i["ident"]))
        for o in outputs:
            w(" {} |".format(o["ident"]))
        for o in oracles:
            if o in failed_oracles:
                w(" *{}* |".format(o["name"]))
            else:
                w(" {} |".format(o["name"]))
        w("\n")
        w("|")
        for i in inputs:
            w(":--:|")
        for o in outputs:
            w(":--:|")
        for o in oracles:
            w(":--:|")
        w("\n")

        index = 0
        while index < length:
            w("|")
            if index == failure_index:
                for i in inputs:
                    w(" **{}** |".format(i["seq"][index]))
                for o in outputs:
                    w(" **{}** |".format(o["seq"][index]))
            else:
                for i in inputs:
                    w(" {} |".format(i["seq"][index]))
                for o in outputs:
                    w(" {} |".format(o["seq"][index]))
            for o in oracle_outputs:
                if o["oracle"] in failed_oracles:
                    if index == failure_index:
                        w(" **{}** |".format(o["seq"][index]))
                    else:
                        w(" *{}* |".format(o["seq"][index]))
                else:
                    w(" {} |".format(o["seq"][index]))
            w("\n")
            index += 1

        w("\n\n")

        w("## Run details\n\n")

        w("As specified in `{}`:\n".format( context_file ))

        w("* binary \"{}\": `{}`\n".format( binary_name, binary_cmd ))
        for line in binary_desc: w( "  {}\n".format(line) )
        w("\n")

        w("* testcase `{}`\n".format( testcase["file"] ))
        for line in testcase["desc"]: w( "  {}\n".format(line) )
        w("\n")

        w("* oracles:\n")
        for oracle in oracles:
            w("  * {}".format(oracle["name"]))
            if oracle["global"]: w(" (**global**)")
            w(":\n\n")
            for line in oracle["desc"]: w("    {}\n".format(line))
            w("\n")
        w("\n")


    finally:
        if brkdwn_file != None: brkdwn_file.close()
