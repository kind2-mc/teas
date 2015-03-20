"""
Exception module.
"""

class InputSeqExc(Exception):
    def __init__(self, msg, fil3, line, form4t):
        self.msg = msg
        self.file = fil3
        self.line = line
        self.format = form4t

    def __str__(self):
        return "\"{}\" for file {} line {} ({})".format(
            self.msg, self.file, self.line, self.format
        )

class TestCtxtExc(Exception):
    def __init__(self, msg, fil3, form4t):
        self.msg = msg
        self.file = fil3
        self.format = form4t

    def __str__(self):
        return "\"{}\" for file {} ({})".format(
            self.msg, self.file, self.format
        )

class ExecExc(Exception):
    def __init__(self, msg, bin_name, test_name):
        self.msg = msg
        self.bin_name = bin_name
        self.test_name = test_name

    def __str__(self):
        return "\"{}\" when running \"{}\" on \"{}\"".format(
            self.msg, self.bin_name, self.test_name
        )