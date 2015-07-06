"""
Sequences of named and typed values contains
- ``"count"``: the number of value sequences,
- ``"len"``: the length of the sequences of values,
- ``"ids"``: the name of the ``count`` sequences,
- ``"types"``: the types of the ``count`` sequences,
- ``"seq"``: the sequence of ``count``-tuples of ``len`` values.
"""

import csv

from stdout import log, error, new_line

def count(t):
  """The number of sequences in this sequence of values."""
  return t["count"]

def length(t):
  """The length of the sequence of values."""
  return t["len"]

def ids(t):
  """The name of the sequences."""
  return t["ids"]

def types(t):
  """The types of the sequences."""
  return t["types"]

def seq(t):
  """The sequence of values."""
  return t["seq"]

def pprint(prefix, t, lvl=2):
  """Prints a sequence of values."""
  # Building a nice string for the signature of the test case.
  idents = ids(t)
  typ3s = types(t)
  # log( "{}idents + typ3s = {}".format(prefix, zip(idents, typ3s)) )
  signature = reduce(
    lambda l,pair: "{}, {}: {}".format(l, pair[0], pair[1]),
    zip(idents[1:], typ3s[1:]),
    "{}: {}".format(idents[0], typ3s[0])
  )
  log( "{}{}".format(prefix, signature), lvl )
  for tup in seq(t):
    pretty = reduce(
      lambda pref, v: "{}, {}".format(pref, v),
      tup[1:],
      tup[0]
    )
    log( "{}| {}".format(prefix, pretty), lvl )

def mk(count, length, ids, types, seq):
  """Creates a sequence of values."""
  return {
    "count": count, "length": length, "ids": ids, "types": types, "seq": seq
  }

def of_csv(path):
  """Creates a sequence of values from a csv file."""
  fil3 = open(path, "rb")
  reader = csv.reader(fil3, delimiter=",")
  reader = map( lambda row: row, reader )
  fil3.close()
  # Extracting info.
  count = len(reader)
  length = len(reader[0]) - 2
  ids = map( lambda row: row[0], reader )
  types = map( lambda row: row[1], reader )
  vals =  map( lambda row: row[2:], reader )
  seq = []
  for row in vals:
    if len(row) != length: raise Exception(
      "file \"{}\" is ill-formed: value sequences are inconsistent".format(
        path
      )
    )
  for i in range(0, length - 1):
    vec = []
    for row in vals:
      vec.append(row[i])
    seq.append(vec)
  return mk(count, length, ids, types, seq)