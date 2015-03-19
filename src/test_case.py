"""
A test case is a list of input sequences.
An input sequence is an ident, a type, and a list of values.
"""

import sys, csv
from stdout import error, log, new_line
from excs import InputSeqExc

# Legal types.
_legal_types = [
    "int", "bool", "real"
]

def legal_types():
    """ Returns the legal types for inputs. """
    return _legal_types

def print_input_seq(ident, typ3, vals, lvl):
    """ Prints an input sequence. """
    log("| ident | {}".format(ident), lvl)
    log("| type  | {}".format(typ3),  lvl)
    log("| seq   | {}".format(vals),  lvl)

def print_test_case(seqs, lvl):
    """ Prints a test case. """
    log("|-------|", lvl)
    for seq in seqs:
        print_input_seq(seq[0], seq[1], seq[2], lvl)
        log("|-------|", lvl)

def _check_input_seq_integrity(
    seq, length, line, file_name, format
):
    """ Checks the integrity of an input sequence.
    The length of the sequence should be the same as the input
    length. """
    seq_length = len(seq)
    if (length is None) and (seq_length < 3):
        raise InputSeqExc(
            "Illegal input sequence has less than 3 \
            columns",
            file_name,
            line,
            form4t
        )
    elif (not (length is None)) and (seq_length != length):
        raise InputSeqExc(
            "Inconsistent test case, first input sequence(s) \
            are {} inputs long but found a sequence of length \
            {}".format(length, seq_length - 2),
            file_name,
            line,
            form4t
        )



def _input_seq_of_csv_row(row, length, line, file_name):
    """ Converts a row from a csv file to an input sequence.
    The row should be an ident, a type, and a sequence of values.
    Checks the integrity of the input sequence, i.e. fails if
    ``length`` is defined and the input sequence has not length
    ``length``.
    Checks if the type is a legal type. """

    # Legal rows must have at least 3 elements.
    if len(row) < 3: raise InputSeqExc(
        "Expecting an identifier, a type, and a sequence of values \
        but found {}".format(row),
        file_name,
        line,
        "csv"
    )

    # Checking integrity if ``length`` is defined.
    elif not (length is None): _check_input_seq_integrity(
        row[2:], length, line, file_name, "csv"
    )

    # Extracting input ident, type, and values of the input sequence.
    ident = row[0]
    typ3 = row[1]
    vals = row[2:]

    # Checking that ``typ3`` is a legal type.
    if not (typ3 in _legal_types): raise InputSeqExc(
        "Unsupported type \"{}\" for input \"{}\"".format(
            typ3, ident
        ),
        file_name,
        line,
        "csv"
    )

    # Returning input sequence as a triplet.
    return ( ident, typ3, vals )


def of_csv_file(file_name):
    """ Reads a csv file and extracts a test case out of it.
    A test case is a list of input sequence.
    An input sequence is an ident, a type, and a list of values. """

    try:
        # Open in read only.
        fil3 = open(file_name, "rb")
        # Not tweaking the reader: ``sep=','`` and ``quote='\"'``.
        reader = csv.reader(fil3)

    except IOError as e: raise InputSeqExc(
        "IOError({}): {}".format(e.errno, e.strerror),
        file_name,
        0,
        "csv"
    )

    else:

        def row_to_input_seq(info, row):
            """ Checks well-foundedness and integrity, and formats
            the input sequence. Used to reduce the rows of the csv
            reader.
            Argument ``info`` is a triplet: previous line index,
            length of the value sequences seen so far, and list
            of input sequences constructed so far."""
            line_count = info[0] + 1
            length = info[1]
            seqs = info[2]
            triplet = _input_seq_of_csv_row(
                row, length, line_count, file_name
            )
            # Setting length.
            length = len(triplet[2])
            seqs.append(triplet)
            # Returning formatted input sequence.
            return (line_count, length, seqs)

        # Convert each row to an input sequence.
        reduced = reduce(
            row_to_input_seq,
            reader,
            # Initially previous line count is 0, length of previous
            # value sequences is undefined, and there is no input
            # sequence.
            (0, None, [])
        )

        # Returning final list of input sequences.
        return reduced[2]

    # Whatever happens we should close the file we opened.
    finally: fil3.close()

