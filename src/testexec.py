"""
A test execution contains
- ``"binary"``: binary to test,
- ``"oracle"``: oracle to use when testing,
- ``"binlog"``: log file for the binary output,
- ``"oralog"``: log file for the oracle output,
- ``"testcase"``: test case to run.
"""

import os, subprocess

from stdout import log
import binary as b
import oracle as o
import values as v
import testcase as tc
import failure as f

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
  file_bin = open( binlog(t), "w" )
  file_ora = open( oralog(t), "w" )

  # Writing headers.
  write_log_header(t, file_bin, file_ora)

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
    testcase = tc.load_values(testcase(t))
    max_k = tc.length(testcase) - 1

    # Result.
    res = None

    # Feeding binary, logging output, feeding oracle, logging output.
    for k in range(0, mak_k):

      # Creating binary input values.
      values = v.seq(testcase)[k]
      values = reduce(
        lambda s,v: s + " " + v,
        values[1:],
        values[0]
      )

      # Feeding binary.
      log( "bin in:  {}".format(values) )
      bin_proc.stdin.write( values )

      # Retrieving binary output.
      output = bin_proc.stdout.read()
      log( "bin out: {}".format(output) )
      out_values = output.split(" ")
      write_out_seq( out_values, file_bin )

      # Creating oracle input values.
      values = values + " " + output

      # Feeding oracle.
      log( "ora in:  {}".format(values) )
      ora_proc.stdin.write( values )

      # Retrieving oracle output.
      output = ora_proc.stdout.read()
      log( "ora out: {}".format(output) )
      out_values = output.split(" ")
      write_out_seq( out_values, file_ora )

      log( "" )

      # Checking the oracle output.
      failure = o.check_values(oracle(t))
      log( "oracle check: {}".format(failure) )
      if failure != None:
        f.add_at(failure, k)
        f.add_testcase(failure, testcase(t))
        f.pprint(failure)
        res = failure
        break

    log( "done" )

  finally:
    # Closing log files.
    file_bin.close()
    file_ora.close()
    # Closing processes if necessary.
    if bin_proc != None: bin_proc.close()
    if ora_proc != None: ora_proc.close()

  return res

