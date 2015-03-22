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
import shlex

from stdout import log, new_line, error, info, warning
from excs import TestCtxtError
import iolib, flags

max_log = flags.max_log_lvl()

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
    else: raise TestCtxtError(
        "{} element number {} has no \"{}\" attribute".format(
            kind, count, att
        ),
        fil3,
        "xml"
    )

def _normalize_cmd(cmd):
    """ Splits a command and formats the path to the binary. """
    split = shlex.split(cmd)
    split[0] = iolib.norm_path(split[0])
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
        else: raise TestCtxtError(
            ("expected bool value for global flag but "
            "found \"{}\" (in oracle number {})").format(
                glob, count
            ),
            fil3,
            "xml"
        )
    except TestCtxtError: return False

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
        "file": iolib.norm_path(path),
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

def _sanitize_binaries(binaries, context_file):
    """ If two binaries

    - have the same command, remove the second one;
    - have the same name but have different commands, rename the second one.

    If any of the above applies, take action and return new list of binaries
    with a flag saying something changed. The reason is that an action can
    break the sanity of previously checked binaries. """
    re_sanitize = False
    original_len = len(binaries)
    # Binaries inspected so far.
    binaries_suffix = []

    # Sanitizing binaries.
    while len(binaries) > 0:

        # If we already changed something, just copy ``binaries`` to
        # ``binaries_suffix``.
        if re_sanitize:
            binary = binaries.pop()
            binaries_suffix.append(binary)
            continue

        binary2 = binaries.pop()
        name2 = binary2["name"]
        cmd2 = binary2["cmd"]

        # Command check.

        have_same_cmd = filter(
            (lambda bn: cmd2 == bn["cmd"]), binaries_suffix
        )
        l_cmd = len(have_same_cmd)

        if l_cmd > 1:
            # Unreachable.
            assert False

        elif l_cmd == 1:
            # Redundancy detected.
            re_sanitize = True
            binary1 = have_same_cmd[0]
            name1 = binary1["name"]

            warning( "Redundant binaries detected in \"{}\"".format(
                context_file
            ) )
            warning( "> \"{}\" and \"{}\"".format( name1, name2 ) )
            warning( "use the same command" )
            warning( "> \"{}\"".format( cmd ) )
            warning( "Removing the second one." )
            # Skipping the rest of this iteration (forgetting ``binary2``).
            continue

        else:
            # No redundancy.
            pass

        # Name check.

        have_same_name = filter(
            (lambda bin: name2 == bin["name"]), binaries_suffix
        )
        l_name = len(have_same_name)

        if l_name > 1:
            # Unreachable.
            assert False

        elif l_name == 1:
            # Redundancy detected.
            re_sanitize = True
            nu_name = "{}_2".format(name2)

            warning( "Binaries with identical names detected in \"{}\"".format(
                context["file"]
            ) )
            warning( "> \"{}\"".format( name2 ) )
            warning( "but use different command. Renaming second one to" )
            warning( "> \"{}\"".format( nu_name ) )
            binary2["name"] = nu_name

        else:
            # No redundancy.
            pass

        # Passed command check, keeping ``binary2`` (potentially renamed).
        binaries_suffix.append(binary2)

    # At this point ``binaries`` should be empty.
    assert len(binaries) == 0

    # Restoring original order.
    binaries_suffix.reverse()

    # Either we removed an element and should re-sanitize...
    if re_sanitize: assert len(binaries_suffix) == original_len - 1
    # ... or we did nothing.
    else: assert len(binaries_suffix) == original_len

    return (re_sanitize, binaries_suffix)

def _sanitize_testcases(testcases, context_file):
    """ If two test cases point to the same file remove the second one and
    return updated list of testcases with a flag saying something changed.
    """
    re_sanitize = False
    original_len = len(testcases)
    # Test cases inspected so far.
    testcases_suffix = []

    # Sanitizing test cases.
    while len(testcases) > 0:

        # If we already changed something, just copy ``testcases`` to
        # ``testcases_suffix``.
        if re_sanitize:
            testcase = testcases.pop()
            testcases_suffix.append(testcase)
            continue

        testcase2 = testcases.pop()
        file2 = testcase2["file"]
        name2 = testcase2["name"]

        have_same_file = filter(
            (lambda tc: file2 == tc["file"]), testcases_suffix
        )
        l_file = len(have_same_file)

        if l_file > 1:
            # Unreachable.
            assert False

        elif l_file == 1:
            re_sanitize = True
            testcase1 = have_same_cmd[0]
            name1 = testcase1["name"]

            warning( "Redundant test cases detected in \"{}\"".format(
                context_file
            ) )
            warning( "> \"{}\" and \"{}\"".format( name1, name2 ) )
            warning( "point to the same file" )
            warning( "> \"{}\"".format( file2 ) )
            warning( "Removing the second one." )
            # Skipping the rest of this iteration (forgetting ``testcase2``).
            continue

        else:
            # No redundancy.
            pass

        # Passed file name check, keeping ``testcase2``.
        testcases_suffix.append(testcase2)

    # At this point ``testcases`` should be empty.
    assert len(testcases) == 0

    # Restoring original order.
    testcases_suffix.reverse()

    # Either we removed an element and should re-sanitize...
    if re_sanitize: assert len(testcases_suffix) == original_len - 1
    # ... or we did nothing.
    else: assert len(testcases_suffix) == original_len

    return (re_sanitize, testcases_suffix)

def sanitize(context, lvl=max_log):
    """ If two binaries

    - have the same command, remove the second one;
    - have the same name but have different commands, rename the second one.

    If two test cases point to the same file, remove the second one.

    Iterate binary check until fixed-point, same for test cases. """
    context_file = context["file"]

    binaries = context["binaries"]
    should_sanitize_binaries = True
    log( "Sanitizing binaries for \"{}\".".format(context["file"]), lvl )
    while should_sanitize_binaries:
        should_sanitize_binaries, binaries = _sanitize_binaries(
            binaries, context_file
        )

    # Updating context with new binaries.
    context["binaries"] = binaries

    testcases = context["testcases"]
    should_sanitize_testcases = True
    log( "Sanitizing test cases.", lvl )
    while should_sanitize_testcases:
        should_sanitize_testcases, testcases = _sanitize_testcases(
            testcases, context_file
        )

    # Updating context with new testcases.
    context["testcases"] = testcases

    return context
