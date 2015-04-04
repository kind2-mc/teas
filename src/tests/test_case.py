""" Tests test case related things. """

from os.path import relpath
from nose.tools import *

import src.test_case as tc

def _get_path(file):
    """ OS safe construction of the path to test file. """
    return relpath( "resources/{}".format(file) )

def _get_csv_path(file):
    """ OS safe construction of the path to a csv test file. """
    return _get_path( "csv/{}.csv".format(file) )



def test_csv_ok_3_lines_6_values():
    """ [CSV] Test case construction (ok, simple). """
    (test_case,length) = tc.of_csv(
        _get_csv_path("ok_3_lines_6_values")
    )

    print("{}".format(test_case))
    assert len(test_case) == 3

    def six_values(testcase):
        """ Checks that sequence in a testcase has length 6. """
        assert len(testcase["seq"]) == 6

    map( six_values, test_case )

@raises(tc.InputSeqError)
def test_csv_fail_illegal_line():
    """ [CSV] Test case construction (fail, illegal line) """
    tc.of_csv( _get_csv_path("fail_illegal_line") )

@raises(tc.InputSeqError)
def test_csv_fail_inconsistent_sequences():
    """ [CSV] Test case construction (fail, inconsistent) """
    tc.of_csv( _get_csv_path("fail_inconsistent_sequences") )

@raises(tc.InputSeqError)
def test_csv_fail_illegal_type():
    """ [CSV] Test case construction (fail, illegal type) """
    tc.of_csv( _get_csv_path("fail_illegal_type") )

    
def _type_check_should_fail(i):
    """ Catches a type error. """
    try: tc.type_check( i )
    except TypeError: assert True
    else: assert False

def test_type_check_bool():
    """ Type check function for bool """
    def test(i): return [ {
        "ident": "test",
        "type": "bool",
        "seq": i
    } ]

    # Should work.
    tc.type_check( test([ "false", "true" ]) )
    
    # Should fail.
    _type_check_should_fail( test([ "True" ]) )
    _type_check_should_fail( test([ "False" ]) )
    _type_check_should_fail( test([ "bla" ]) )
    _type_check_should_fail( test([ "bli" ]) )
    _type_check_should_fail( test([ "0" ]) )
    _type_check_should_fail( test([ "1" ]) )
    _type_check_should_fail( test([ "42" ]) )

def test_type_check_int():
    """ Type check function for int """
    def test(i): return [ {
        "ident": "test",
        "type": "int",
        "seq": i
    } ]

    # Should work.
    tc.type_check( test([ "0", "42", "17" ]) )
    
    # Should fail.
    _type_check_should_fail( test([ "true" ]) )
    _type_check_should_fail( test([ "false" ]) )
    _type_check_should_fail( test([ "True" ]) )
    _type_check_should_fail( test([ "False" ]) )
    _type_check_should_fail( test([ "0." ]) )
    _type_check_should_fail( test([ "17", "3", "69.1" ]) )
    _type_check_should_fail( test([ "bla", "41" ]) )

def test_type_check_float():
    """ Type check function for float """
    def test(i): return [ {
        "ident": "test",
        "type": "float",
        "seq": i
    } ]

    # Should work.
    tc.type_check( test([ "0.72503", "42.7", "17." ]) )
    
    # Should fail.
    _type_check_should_fail( test([ "true" ]) )
    _type_check_should_fail( test([ "false" ]) )
    _type_check_should_fail( test([ "True" ]) )
    _type_check_should_fail( test([ "False" ]) )
    _type_check_should_fail( test([ "0" ]) )
    _type_check_should_fail( test([ "7.17", "0.3", "69" ]) )
    _type_check_should_fail( test([ "bla", "1.41" ]) )