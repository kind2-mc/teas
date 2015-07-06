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

from stdout import log
import testcase as tc

def modes(t):
  """The modes the implications of which were falsified."""
  return t["modes"]

def globals(t):
  """The global contracts for which the ensure was false."""
  return t["globals"]

def mode_reqs(t):
  """Indicates if at least one mode requirement evaluated to true during the
  failure."""
  return t["mode_reqs"]

def global_reqs(t):
  """The global contracts the requirement of which were falsified."""
  return t["global_reqs"]

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
  if len(modes(t)) > 0:
    log( "{}| modes:       {}".format(prefix, modes(t)), lvl )
  if len(globals(t)) > 0:
    log( "{}| globals:     {}".format(prefix, globals(t)), lvl )
  if not mode_reqs(t):
    log( "{}| mode_reqs:   {}".format(prefix, mode_reqs(t)), lvl )
  if len(global_reqs(t)) > 0:
    log( "{}| global_reqs: {}".format(prefix, global_reqs(t)), lvl )
  if testcase(t) != None:
    log( "{}| for testcase:".format(prefix), lvl )
    tc.pprint( "{}| | ".format(prefix), testcase(t), lvl )

def mk(modes, glob4ls, mode_reqs, glob4l_reqs):
  """Creates a failure with no ``at`` nor ``testcase`` field."""
  if (
    len(modes) == 0 and len(glob4ls) == 0 and
    mode_reqs and len(glob4l_reqs) == 0
  ): return None
  else: return {
    "modes": modes, "globals": glob4ls,
    "mode_reqs": mode_reqs, "global_reqs": glob4l_reqs
  }

def add_at(t, k):
  """Adds a ``"at"`` field to a failure."""
  if "at" in t.keys():
    log("at: {}".format(t["at"]))
    raise Exception(
      "cannot add \"at\" field, it is already defined"
    )
  t["at"] = k

def add_testcase(t, test_case):
  """Adds a ``"testcase"`` field to a failure."""
  if "testcase" in t.keys(): raise Exception(
    "cannot add \"testcase\" field, it is already defined"
  )
  t["testcase"] = test_case




