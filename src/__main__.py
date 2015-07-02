""" Entry point. """

import sys, os, multiprocessing, time

from stdout import new_line, log, error, warning, info
import lib, iolib, options, flags
import test_case, test_context
import context as ctxt
import binary as bina
import testexec, testset, binary
import execution, breakdown

max_log = flags.max_log_lvl()

def init():
  """ Parses command-line arguments and sets up the configuration.
  Returns the list of existing test context files to run on. """

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
      warning(
          "Skipping input file \"{}\" (does not exist).".format(path)
      )
      new_line(1)
      return False

  # Discarding duplicates and inexistant files.
  def rm_duplicates_and_inexistant(li5t, path):
    if path in li5t: return li5t
    elif file_exists(path):
      li5t.append(path)
      return li5t
    else: return li5t

  # Cleaning list of files.
  files = reduce( rm_duplicates_and_inexistant, all_files, [] )

  # Adding binaries requested by the user.
  for triple in flags.binaries_to_add():
    n = triple[0]
    cmd = triple[1]
    path = triple[2]
    log(
        "Adding binary (\"{}\", \"{}\") to test context \"{}\".".format(
            n, cmd, path
        )
    )
    ctxt.add_binary(path, bina.mk(n, cmd))
    log("Done.")
    new_line()

  # Exiting if no file to run on.
  if len(files) < 1:
    warning("No file to run on, done.")
    new_line(1)
    sys.exit(0)

  # Create output directory if necessary.
  try: iolib.mkdir(flags.out_dir())
  except iolib.IOLibError as e:
    error("while creating output directory:")
    error("> {}".format(e.msg))
    new_line(0)
    sys.exit(1)

  return files

def get_contexts(files):
  """Creates and returns the test contexts from some files."""

  test_contexts = []

  for fil3 in files:
    log("Parsing test context from \"{}\".".format(fil3))
    context = ctxt.of_file(fil3)
    log("Success:")
    ctxt.pprint("  ", context)
    new_line()
    # Don't load the testcase itself, we do that right before running the
    # test itself.
    test_contexts.append(context)

  new_line()
  return test_contexts

def load_testcase(test_execution):
  """ Loads the test case from the test case file. """
  # Only loading if necessary.
  testcase = test_execution["testcase"]
  if "inputs" not in testcase:
    testcase_path = testcase["file"]
    (input_seq, length) = test_case.of_file(testcase_path)
    testcase["inputs"] = input_seq
    testcase["length"] = length
    test_case.print_test_case(input_seq, max_log)
    new_line(max_log)

def run_test(test_execution):
  """ Runs a test. """
  ok = execution.run(test_execution)
  return ok

# Safety thing for parallelism.
if __name__ == "__main__":

  # Handling command-line arguments, getting existing test context files.
  files = init()

  out_dir = flags.out_dir()

  # Creating test execution structures, creating log directory.
  # test_executions = get_test_executions(files)
  test_contexts = get_contexts(files)
  # job_count = len(test_executions)

  for test_context in test_contexts:

    for bin4ry in ctxt.bins(test_context):
      log( "Running tests for system {}".format(
          ctxt.system(test_context)
      ) )
      log( "  {} test sets".format(len(ctxt.tests(test_context))) )
      log( "  on binary" )
      binary.pprint("    ", bin4ry)
      new_line(max_log)

      oracle = ctxt.oracle(test_context)

      def run_test(test_case):
        test_exec = testexec.mk(bin4ry, oracle, out_dir, test_case)
        return testexec.run(test_exec)

      for test_set in ctxt.tests(test_context):
        log( "Loading test set {}".format(test_set) )
        ts = testset.of_file(test_set)
        log( "Done, setting up test set \"{}\".".format(testset.name(ts)) )
        new_line(max_log)

        job_count = len( testset.tests(ts) )

        if flags.run_tests():

          if flags.sequential_run():
            log("  Sequential run, {} jobs.".format(job_count))
            res_list = map(run_test, testset.tests(ts))
            total = len(res_list)
            successes = len( [ok for ok in res_list if ok] )
            failures = total - successes
            width = len(str(total))
            log("  Done on {} tests:".format(total))
            log("    > \033[32m{0:>{width}} test passed\033[0m".format(
              successes, width=width)
            )
            if failures > 0:
              log("    > \033[31m{0:>{width}} test failed\033[0m".format(
                failures, width=width)
              )

          else:
            log("  Running {} jobs in parallel with {} workers.".format(
              job_count, flags.max_proc()
            ))
            new_line(max_log)
            p00l = multiprocessing.Pool(flags.max_proc())
            res_list = p00l.map(run_test, testset.tests(ts))
            total = len(res_list)
            successes = len( [ok for ok in res_list if ok] )
            failures = total - successes
            width = len(str(total))
            log("  Done on {} tests:".format(total))
            log("    > \033[32m{0:>{width}} test passed\033[0m".format(
              successes, width=width)
            )
            if failures > 0:
              log("    > \033[31m{0:>{width}} test failed\033[0m".format(
                failures, width=width)
              )
          new_line()
          new_line()


  new_line()
  log("Done.")
  new_line(1)
