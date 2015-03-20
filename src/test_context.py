""" A test context is a list of \"binaries\", a list of \"oracles\",
and a list of \"test cases\".

A \"binary\"
  is a pair of the path to the binary, and a description.

An \"oracle\"
  is a path to the oracle, a name, a global flag, and a description.

A \"test case\"
  is a path to the test case, a name, a format (e.g. \"csv\"), and
  a description.
"""

import xml.etree.ElementTree as xet
import os

from stdout import log, new_line, error, info
from excs import TestCtxtExc

def _print_binary(binary, lvl):
    """ Prints a binary from a test context. """
    path = binary[0]
    log( "  > {}".format(path), lvl )

def _print_oracle(oracle, lvl):
    """ Prints an oracle from a test context. """
    path = oracle[0]
    name = oracle[1]
    glob = oracle[2]
    log( "  > ({}) {} | {}".format(
        glob, name, path
    ), lvl )

def _print_testcase(testcase, lvl):
    """ Prints a test case from a test context. """
    path = testcase[0]
    name = testcase[1]
    frmt = testcase[2]
    log( "  > ({}) {} | {}".format(
        frmt, name, path
    ), lvl)

def print_test_context(context, lvl=2):
    """ Prints a test context. """
    binaries = context[0]
    oracles = context[1]
    testcases = context[2]

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

def _binary_of_xml(tree, count, fil3):
    """ Creates a binary from an xml tree.
    A binary is a pair of the path, and a description. """

    path = _attribute_of_xml(tree, "path", "binary", count, fil3)
    return ( path, tree.text )

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

    path = _attribute_of_xml(tree, "path", "oracle", count, fil3)
    name = _attribute_of_xml(tree, "name", "oracle", count, fil3)
    glob = _global_flag_of_xml(tree, count, fil3)

    return ( path, name, glob, tree.text )

def _testcase_of_xml(tree, count, fil3):
    """ Creates a test case from an xml tree.
    A test case is a path, a name, a format, and a description. """

    path = _attribute_of_xml(tree, "path", "test case", count, fil3)
    name = _attribute_of_xml(tree, "name", "test case", count, fil3)
    form4t = _attribute_of_xml(
        tree, "format", "test case", count, fil3
    )

    return ( path, name, form4t, tree.text )


def of_xml(path):
    """ Creates a test context from an xml file. """
    xml_tree = xet.parse(path)
    root = xml_tree.getroot()

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

    return ( binary_list, oracle_list, testcase_list )
