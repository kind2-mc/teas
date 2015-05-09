"""
Module for the context of test execution for a system. A context contains
- ``"system"``: the name of the original system,
- ``"oracle"``: the oracle for that system,
- ``"tests"``: a sequence of paths to the test sets for that system.
"""

import xml.etree.ElementTree as xet

import binary as b
import testset as ts
import oracle as oracl3
from stdout import log, error, new_line

def system(t):
  """The system of a context."""
  return t["system"]

def oracle(t):
  """The oracle of a context."""
  return t["oracle"]

def tests(t):
  """The test sets of a context."""
  return t["tests"]

def bins(t):
  """The binaries of a context."""
  return t["bins"]

def pprint(prefix, t, lvl=2):
  """Prints a context."""
  log( "{}{}".format(prefix, system(t)), lvl )
  log( "{}| oracle:".format(prefix), lvl )
  oracl3.pprint("{}|  ".format(prefix), oracle(t), lvl)
  log( "{}| test sets:".format(prefix), lvl )
  for test in tests(t):
    log( "{}|  {}".format(prefix, test), lvl )
  log( "{}| binaries:".format(prefix), lvl )
  for binar in bins(t):
    log( "{}|  {}".format(prefix, binar), lvl )

def mk(system, oracle, tests, bins):
  """Creates a context."""
  return {
    "system": system, "oracle": oracle, "tests": tests, "bins": bins
  }


def of_xml(tree):
  """Creates a context from an xml tree."""
  if "system" not in tree.attrib.keys(): raise Exception(
    "illegal test file: data tag misses a system attribute"
  )
  system = tree.attrib["system"]
  oracle = oracl3.of_xml(tree)
  test_sets = map(
    (lambda t: t.text),
    tree.findall("tests")
  )
  bins = map(
    (lambda tree: b.of_xml(tree)),
    tree.findall("binary")
  )
  return mk(system, oracle, test_sets, bins)

def of_file(path):
  """Creates a context from an xml file."""
  xml_tree = xet.parse(path)
  root = xml_tree.getroot()
  return of_xml(root)

def testset_num(t, i):
  """Loads and returns the ``i``th test set in the context."""
  return ts.of_file( tests(t)[i] )

def add_binary(path, bin4ry):
  """Loads the context stored in a file and adds the binary as field to it."""
  tree = xet.parse(path)
  root = tree.getroot()
  new_bin4ry = xet.Element("binary")
  new_bin4ry.set("name", b.name(bin4ry))
  new_bin4ry.text = b.cmd_joined(bin4ry)
  root.append(new_bin4ry)
  tree.write(path)


# fil3 = "/Volumes/home/uchuu/runs/testgen2/PFS/tests.xml"
# xml_tree = xet.parse(fil3)
# root = xml_tree.getroot()

# context = of_xml(root)
# log( "" )
# pprint("", context)
# log( "" )

# log( "Loading test sets" )
# test_sets = map(
#   testset.of_file,
#   tests(context)
# )
# log( "done" )
# log( "" )

# for test_set in test_sets:
#   testset.pprint("", test_set)
#   log( "" )

#   log( "loading values" )
#   log( "" )

#   for test_case in testset.tests(test_set):
#     vals = testcase.load_values(test_case)
#     values.pprint("", vals)
#     log( "" )
