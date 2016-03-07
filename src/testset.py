"""
A test set contains
- ``"system"``: system the tests were generated from,
- ``"name"``: name of the test set,
- ``"testcases"``: a list of testcases.
"""

import xml.etree.ElementTree as xet
import os

import testcase
import testexec
from stdout import log, error, new_line

def system(t):
  """The system of a test set."""
  return t["system"]

def name(t):
  """The name of a test set."""
  return t["name"]

def tests(t):
  """The test cases of a test set."""
  return t["tests"]

def pprint(prefix, t, lvl=2):
  """Prints a test set."""
  log( "{}{}".format(prefix, name(t)), lvl )
  log( "{}| {}".format(prefix, system(t)), lvl )
  log( "{}| test cases:".format(prefix), lvl )
  for test_case in tests(t):
    testcase.pprint("{}| | ".format(prefix), test_case)

def mk(system, name, tests):
  """Creates a test set."""
  return { "system": system, "name": name, "tests": tests }

def of_xml(tree, path):
  """Creates a test set from an xml tree."""
  if "system" not in tree.attrib.keys(): raise Exception(
    "illegal test set file: data tag misses a system attribute"
  )
  if "name" not in tree.attrib.keys(): raise Exception(
    "illegal test set file: data tag misses a name attribute"
  )
  # Extracting info.
  system = tree.attrib["system"]
  name = tree.attrib["name"]
  testcases = map(
    lambda tc: testcase.of_xml(tc, path),
    tree.findall("testcase")
  )
  # Done.
  return mk(system, name, testcases)

def of_file(path):
  """Creates a test set from a file."""
  tree = xet.parse(path)
  root = tree.getroot()
  return of_xml(root, os.path.abspath(os.path.join(path, os.pardir)))

# def to_testexecs(t, binary, oracle, log_root):
#   """Returns a list of test executions, one for each test case of the test
#   set."""
#   return map(
#     lambda tc: testexec.mk(binary, oracle, log_root, tc),
#     tests(t)
#   )

