"""
A testcase contains
- ``"path"``: the path to the actual test case,
- ``"name"``: the name of the test case,
- ``"format"``: the format of the actual test case,
- ``"description"``: a list of lines describing the test case.
"""

import values
from stdout import log, error, new_line

def path(t):
  """The path to the actual test case."""
  return t["path"]

def name(t):
  """The name of a test case."""
  return t["name"]

def format(t):
  """The format of the actual test case file."""
  return t["format"]

def desc(t):
  """The description of a test case."""
  return t["desc"]

def pprint(prefix, t, lvl=2):
  """Prints a test case."""
  log( "{}{}".format(prefix, name(t)), lvl )
  log( "{}| {} ({})".format(prefix, path(t), format(t)), lvl )
  log( "{}| description:".format(prefix), lvl )
  for line in desc(t):
    log( "{}| | {}".format(prefix, line), lvl )

def mk(path, name, form4t, desc):
  """Creates a test case."""
  return { "path": path, "name": name, "format": form4t, "desc": desc }

def of_xml(tree, path):
  """Creates a test case from an xml tree."""
  if "path" not in tree.attrib.keys(): raise Exception(
    "illegal test set file: data tag missing a path attribute"
  )
  if "name" not in tree.attrib.keys(): raise Exception(
    "illegal test set file: data tag missing a name attribute"
  )
  if "format" not in tree.attrib.keys(): raise Exception(
    "illegal test set file: data tag missing a format attribute"
  )
  # Extracting info.
  path = "{}/{}".format(path, tree.attrib["path"])
  name = tree.attrib["name"]
  form4t = tree.attrib["format"]
  desc = map( lambda s: s.strip(), tree.text.split("\n") )
  # Cleaning the description.
  if len(desc) > 0 and desc[0] == "":
    desc = desc[1:]
  if len(desc) > 0 and desc[-1] == "":
    desc = desc[:-1]
  # Done.
  return mk(path, name, form4t, desc)

def load_values(t):
  """Loads the values from the file associated with a test case."""
  if format(t) != "csv": raise Exception(
    "unsupported format for values \"{}\", only csv is supported".format(
      format(t)
    )
  )
  return values.of_csv(path(t))
