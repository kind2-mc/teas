"""
A test execution contains
- ``"binary"``: binary to test,
- ``"oracle"``: oracle to use when testing,
- ``"binlog"``: log file for the binary output,
- ``"oralog"``: log file for the oracle output,
- ``"testcase"``: test case to run.
"""

import os, subprocess

from stdout import log, new_line
import binary as b
import oracle as o
import values as v
import testcase as tc
import failure as f
import flags

max_log = flags.max_log_lvl()

def binary(t):
  """The binary of a test execution."""
  return t["binary"]

def oracle(t):
  """The oracle to use when testing."""
  return t["oracle"]

def binlog(t):
  """The log file for the binary output."""
  return t["binlog"]

def oralog(t):
  """The log file for the oracle output."""
  return t["oralog"]

def testcase(t):
  """The test case to run."""
  return t["testcase"]

def pprint(prefix, t, lvl=2):
  """Prints a test execution."""
  log(
    "{}execution with log {} / {}".format(prefix, binlog(t), oralog(t)), lvl
  )
  log( "{}| binary:".format(prefix), lvl )
  b.pprint( "{}| | ".format(prefix), binary(t), lvl )
  log( "{}| oracle:".format(prefix), lvl )
  o.pprint( "{}| | ".format(prefix), oracle(t), lvl )
  log( "{}| testcase:".format(prefix), lvl )
  tc.pprint( "{}| | ".format(prefix), testcase(t), lvl )

def mk(binary, oracle, log_root, testcase):
  """Creates a test execution."""
  name = tc.name(testcase)
  log_prefix = log_root + "/" + name
  return {
    "binary": binary,
    "oracle": oracle,
    "binlog": log_prefix + ".binary.csv",
    "oralog": log_prefix + ".oracle.csv",
    "testcase": testcase
  }

def write_log_header(t, file_bin, file_ora):
  """Writes the header for the binary output log and the oracle output log
  files."""
  # Helper functions for writing.
  def w_bin(s): file_bin.write(s)
  def w_ora(s): file_ora.write(s)
  def w(s):
    w_bin(s)
    w_ora(s)
  # Writing stuff.
  w_bin( "# Output of binary {}\n#\n".format(b.name(binary(t))) )
  w_ora( "# Output of oracle for binary {}\n#\n".format(b.name(binary(t))) )
  w(
    (
      "# binary command: \"{}\"\n"
      "# testcase: {}\n"
      "# | {}\n#\n"
    ).format(
      b.cmd_joined(binary(t)),
      tc.name(testcase(t)),
      tc.path(testcase(t)),
    )
  )

def write_out_seq(values, fil3):
  """Writes a sequence of values in CSV in a file."""
  values = reduce(
    lambda s,v: s + "," + v,
    values[1:],
    values[0]
  )
  fil3.write( values + "\n" )

def run(t):
  """Runs a test execution."""
  # Opening log files
  # file_bin = open( binlog(t), "w" )
  # file_ora = open( oralog(t), "w" )

  # Writing headers.
  # write_log_header(t, file_bin, file_ora)

  # Creating processes.
  bin_proc = None
  ora_proc = None

  try:

    bin_proc = subprocess.Popen(
      b.cmd(binary(t)),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )
    ora_proc = subprocess.Popen(
      o.path(oracle(t)),
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE
    )

    # Loading test case.
    log( "    loading test case \"{}\"".format(tc.name(testcase(t))), max_log )
    test_case = tc.load_values(testcase(t))
    max_k = len( v.seq(test_case) ) - 1

    # Result.
    res = None

    # Feeding binary, logging output, feeding oracle, logging output.
    for k in range(0, max_k):

      log( "    step {}".format(k), max_log )

      # Creating binary input values.
      values = v.seq(test_case)[k]
      values = reduce(
        lambda s,v: s + " " + v,
        values[1:],
        values[0]
      )

      # Feeding binary.
      log( "      bin in:  {}".format(values), max_log )
      bin_proc.stdin.write( values + "\n" )

      # Retrieving binary output.
      output = bin_proc.stdout.readline().strip()
      log( "      bin out: {}".format(output), max_log )
      out_values = output.split(" ")
      # write_out_seq( out_values, file_bin )

      # Creating oracle input values.
      values = values + " " + output

      # Feeding oracle.
      log( "      ora in:  {}".format(values), max_log )
      ora_proc.stdin.write( values + "\n" )

      # Retrieving oracle output.
      output = ora_proc.stdout.readline().strip()
      log( "      ora out: {}".format(output), max_log )
      out_values = output.split(" ")
      # write_out_seq( out_values, file_ora )

      # Checking the oracle output.
      failure = o.check_values(oracle(t), out_values)
      if failure != None:
        f.add_at(failure, k)
        f.add_testcase(failure, testcase(t))
        f.pprint("    ", failure, max_log)
        res = failure
        break
      else:
        log( "      oracle check: ok", max_log )

    log( "    done", max_log )
    new_line( max_log )

  finally:
    # Closing log files.
    # file_bin.close()
    # file_ora.close()
    # Closing processes if necessary.
    if bin_proc != None:
      bin_proc.stdin.close()
      bin_proc.stdout.close()
      bin_proc.stderr.close()
    if ora_proc != None:
      ora_proc.stdin.close()
      ora_proc.stdout.close()
      ora_proc.stderr.close()

  return res == None

