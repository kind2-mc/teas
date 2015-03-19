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
    test_case = tc.of_csv_file(
        _get_csv_path("ok_3_lines_6_values")
    )

    assert len(test_case) == 3

    def six_values(triplet):
        """ Checks that the third element of a triplet has length 
        6. """
        assert len(triplet[2]) == 6

    map( six_values, test_case )

@raises(tc.InputSeqExc)
def test_csv_fail_illegal_line():
    """ [CSV] Test case construction (fail, illegal line). """
    tc.of_csv_file( _get_csv_path("fail_illegal_line") )

@raises(tc.InputSeqExc)
def test_csv_fail_inconsistent_sequences():
    """ [CSV] Test case construction (fail, inconsistent). """
    tc.of_csv_file( _get_csv_path("fail_inconsistent_sequences") )

@raises(tc.InputSeqExc)
def test_csv_fail_illegal_type():
    """ [CSV] Test case construction (fail, illegal type). """
    tc.of_csv_file( _get_csv_path("fail_illegal_type") )