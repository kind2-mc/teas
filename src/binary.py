"""
A binary contains
- ``"name"``: the name of the binary,
- ``"cmd"``: the command to run the binary.
"""

import lib, iolib

from stdout import log

def name(t):
  """The name of the binary."""
  return t["name"]

def cmd(t):
  """The command of the binary."""
  return t["cmd"]

def cmd_joined(t):
  """The command of the binary as a string."""
  return lib.string_join(cmd(t))

def pprint(prefix, t, lvl=2):
  """Prints a binary."""
  log( "{}{}".format(prefix, name(t)), lvl )
  log( "{}> {}".format(prefix, cmd_joined(t)), lvl )

def mk(name, cmd):
  """Creates a binary."""
  return {
    "name": name,
    "cmd": iolib.split_cmd(cmd)
  }

def of_xml(tree):
  """Creates a binary from an xml tree."""
  name = tree.attrib["name"]
  cmd = tree.text
  setup = lib.run_setup_if_any(
    tree, "binary \"{}\"".format(name)
  )
  return mk(name, cmd)

def dummy():
  """Creates a dummy binary."""
  return mk("dummy", "dummy")