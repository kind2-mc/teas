""" A test context is a file, a name, a list of \"binaries\", a list
of \"oracles\", and a list of \"test cases\".

A \"binary\" (triplet)
  is a name, a command, and a description.

An \"oracle\" (4-uple)
  is a name, a command, a global flag, and a description.

A \"test case\" (4-uple)
  is a name, a file to the test case, a format (e.g. \"csv\"), and
  a description.
"""

import xml.etree.ElementTree as xet
import os, shlex

from stdout import log, new_line, error, info, warning
from excs import TestCtxtExc
import flags

def _print_binary(binary, lvl):
    """ Prints a binary from a test context. """
    name = binary["name"]
    cmd = binary["cmd"]
    log( "  > {} | {}".format(name, cmd), lvl )

def _print_oracle(oracle, lvl):
    """ Prints an oracle from a test context. """
    name = oracle["name"]
    cmd = oracle["cmd"]
    glob = oracle["global"]
    log( "  > ({}) {} | {}".format(
        glob, name, cmd
    ), lvl )

def _print_testcase(testcase, lvl):
    """ Prints a test case from a test context. """
    name = testcase["name"]
    path = testcase["file"]
    frmt = testcase["format"]
    log( "  > ({}) {} | {}".format(
        frmt, name, path
    ), lvl)

def print_test_context(context, lvl=2):
    """ Prints a test context. """
    name = context["name"]
    binaries = context["binaries"]
    oracles = context["oracles"]
    testcases = context["testcases"]

    log( "\"{}\"".format(name), lvl )
    log( "> binaries:", lvl)
    for binary in binaries: _print_binary(binary, lvl)

    log( "> oracles:", lvl)
    for oracle in oracles: _print_oracle(oracle, lvl)

    log( "> testcases:", lvl)
    for testcase in testcases: _print_testcase(testcase, lvl)


def _attribute_of_xml(tree, att, kind, count, fil3):
    """ Returns attribute ``att`` from ``tree``, fails if it's
    not a valid key. """
    if att in tree.attrib.keys(): return tree.attrib[att]
    else: raise TestCtxtExc(
        "{} element number {} has no \"{}\" attribute".format(
            kind, count, att
        ),
        fil3,
        "xml"
    )

_already_warned = False
def _normalize_path(path):
    """ Formats a path. """
    global _already_warned
    if not _already_warned:
        warning("Path normalization uses \"relpath\".")
        _already_warned = True
    return os.path.relpath(path)

def _normalize_cmd(cmd):
    """ Splits a command and formats the path to the binary. """
    split = shlex.split(cmd)
    split[0] = _normalize_path(split[0])
    return split

def _binary_of_xml(tree, count, fil3):
    """ Creates a binary from an xml tree.
    A binary is a command, a name, and a description. """

    name = _attribute_of_xml(tree, "name", "binary", count, fil3)
    cmd = _attribute_of_xml(tree, "cmd", "binary", count, fil3)
    return {
        "name": name,
        "cmd": _normalize_cmd(cmd),
        "desc": tree.text
    }

def _global_flag_of_xml(tree, count, fil3):
    """ Retrieves the value of the global flag of an xml tree.
    If no \"global\" attribute exists returns \"False\". """
    try:
        glob = _attribute_of_xml(tree, "global", "", "", "")
        if glob in [ "true", "True" ]: return True
        elif glob in [ "false", "False" ]: return False
        else: raise TestCtxtExc(
            ("expected bool value for global flag but "
            "found \"{}\" (in oracle number {})").format(
                glob, count
            ),
            fil3,
            "xml"
        )
    except TestCtxtExc: return False

def _oracle_of_xml(tree, count, fil3):
    """ Creates an oracle from an xml tree.
    An oracle is a path, a global flag, and a description. """

    cmd = _attribute_of_xml(tree, "cmd", "oracle", count, fil3)
    name = _attribute_of_xml(tree, "name", "oracle", count, fil3)
    glob = _global_flag_of_xml(tree, count, fil3)

    return {
        "name": name,
        "cmd": _normalize_cmd(cmd),
        "global": glob,
        "desc": tree.text
    }

def _testcase_of_xml(tree, count, fil3):
    """ Creates a test case from an xml tree.
    A test case is a file, a name, a format, and a description. """

    name = _attribute_of_xml(tree, "name", "test case", count, fil3)
    path = _attribute_of_xml(tree, "path", "test case", count, fil3)
    form4t = _attribute_of_xml(
        tree, "format", "test case", count, fil3
    )

    return {
        "name": name,
        "file": _normalize_path(path),
        "format": form4t,
        "desc": tree.text
    }


def of_xml(path):
    """ Creates a test context from an xml file. """
    xml_tree = xet.parse(path)
    root = xml_tree.getroot()

    # Retrieving context name.
    name = _attribute_of_xml(root, "name", "root", 0, path)

    # Retrieving binaries.
    binary_count = 0
    binary_list = []
    for tree in root.findall("binary"):
        binary_count += 1
        binary = _binary_of_xml(tree, binary_count, path)
        binary_list.append(binary)

    # Retrieving oracles.
    oracle_count = 0
    oracle_list = []
    for tree in root.findall("oracle"):
        oracle_count += 1
        oracle = _oracle_of_xml(tree, oracle_count, path)
        oracle_list.append(oracle)

    # Retrieving test cases.
    testcase_count = 0
    testcase_list = []
    for tree in root.findall("testcase"):
        testcase_count += 1
        testcase = _testcase_of_xml(tree, testcase_count, path)
        testcase_list.append(testcase)

    return {
        "file": path,
        "name": name,
        "binaries": binary_list,
        "oracles": oracle_list,
        "testcases": testcase_list
    }

# Maps extensions to test context creation function.
_extension_map = {
    ".xml": of_xml
}

def of_file(path):
    """ Creates a test context from a file. """

    for extension, function in _extension_map.iteritems():
        if path.endswith(extension):
            log(
                "Detected \"{}\" extension.".format(extension),
                flags.max_log_lvl()
            )
            return function(path)