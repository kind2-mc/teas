"""
Module for the oracle of a system. An oracle contains
- ``"path"``: the path to the binary of the oracle,
- ``"outputs"``: the outputs of the system, i.e. the name of the output and a
  boolean indicating if the output corresponds to a global mode.
"""

from lib import bool_of_string
from iolib import norm_path
from stdout import log, error, new_line

import flags
import failure

max_log = flags.max_log_lvl()

def path(t):
  """The path of an oracle."""
  return t["path"]

def outputs(t):
  """The outputs of the oracle."""
  return t["out"]

def pprint(prefix, t, lvl=2):
  """Prints an oracle."""
  log( "{}{}".format(prefix, path(t)), lvl )
  for out in outputs(t):
    if out[1]:
      suff = " (global)"
    else:
      suff = ""
    log( "{}| {}{}".format(prefix, out[0], suff), lvl )

def mk(path, outputs):
  """Creates an oracle."""
  return { "path": norm_path(path), "out": outputs }

def of_xml(xml_tree):
  """Creates an oracle from an xml element tree. The tree should have an
  ``oracle`` subtree with a ``path`` attribute. The subtree should have some
  ``output`` xml leaves with a ``global`` (boolean) attribute, and its content
  should be the name of the output."""
  for oracle in xml_tree.findall("oracle"):
    # Fail if no path attribute.
    if "path" not in oracle.attrib.keys(): raise Exception(
      "illegal oracle: no path attribute"
    )
    path = oracle.attrib["path"]
    # Extracts output info.
    def extract(leaf):
      if "global" not in leaf.attrib.keys(): raise Exception(
        "illegal oracle: some outputs miss the global flag"
      )
      return ( leaf.text, bool_of_string(leaf.attrib["global"]) )
    outputs = map(extract, oracle.findall("output"))
    return {"path": path, "out": outputs}

def check_values(t, values):
  """Checks if the input values for the oracle makes the contract it
  corresponds to evaluate to true."""
  if 2 * len(outputs(t)) != len(values): raise Exception(
    "dimension mismatch between oracle signature and the values to check"
  )
  outs = outputs(t)
  # Modes the implication of which evaluates to false.
  modes = []
  # The global contracts the ensure of which evaluates to false.
  globs = []
  # Will be set to true if at least one mode evaluate to true.
  mode_reqs = False
  # The global contracts the requirement of which evaluates to false.
  glob_reqs = []

  # Inspecting modes and globals.
  for i in range(0, len(outs)):
    two_i = 2 * i
    fst = bool_of_string(values[two_i])
    snd = bool_of_string(values[two_i+1])
    glob = outs[i][1]
    if not glob:
      if fst: mode_reqs = True
      if not snd: modes.append(outputs(t)[i])
    else:
      # if not fst: glob_reqs.append(i)
      if not snd: globs.append(outputs(t)[i])

  return failure.mk(modes, globs, mode_reqs, glob_reqs)

