"""
A failure is a violation of the contract encoded in an oracle. This means that
at some point during the test case
- one or more global contracts were falsified and/or
- none of the modes evaluate to true.

A failure necessarily contains
- ``"modes"``: true iff one mode or more evaluated to true,
- ``"globals"``: the indices of the global contracts that were falsified.

As a failure is propagated upward from ``check_values`` in the ``oracle``
module to the top level, it will be augmented with
- ``"at"``: the step in the test case where the failure occured,
- ``"testcase"``: the test case on which the failure occured.
"""

import testcase as tc

def modes(t):
  """Indicates if at least one mode evaluated to true during the failure."""
  return t["modes"]

def globals(t):
  """The global contracts that were falsified."""
  return t["globals"]

def at(t):
  """The step at which the failure occured."""
  return t["at"]

def testcase(t):
  """The testcase on which the failure occured."""
  return t["testcase"]

def pprint(prefix, t, lvl=2):
  """Prints a failure."""
  if at(t) != None:
    log( "{}Failure at {}".format(prefix, at(t)), lvl )
  else:
    log( "{}Failure".format(prefix), lvl )
  log( "{}| modes:   {}".format(prefix, modes(t)), lvl )
  log( "{}| globals: {}".format(prefix, globals(t)), lvl )
  if testcase(t) != None:
    log( "{}| for testcase:".format(prefix), lvl )
    tc.pprint( "{}| | ".format(prefix), testcase(t) )

def mk(modes, glob4ls):
  """Creates a failure with no ``at`` nor ``testcase`` field."""
  return { "modes": modes, "globals": glob4ls }

def add_at(t, k):
  """Adds a ``"at"`` field to a failure."""
  if t["at"] != None: raise Exception(
    "cannot add \"at\" field, it is already defined"
  )
  t["at"] = k

def add_testcase(t, test_case):
  """Adds a ``"testcase"`` field to a failure."""
  if t["at"] != None: raise Exception(
    "cannot add \"testcase\" field, it is already defined"
  )
  t["testcase"] = test_case