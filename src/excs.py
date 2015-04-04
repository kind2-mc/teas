"""
Exception module.
"""

class IOLibError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return "[IOLib] {}".format(msg)

class InputSeqError(Exception):
    def __init__(self, msg, fil3, line, form4t):
        self.msg = msg
        self.file = fil3
        self.line = line
        self.format = form4t

    def __str__(self):
        return "[InputSeq] \"{}\" for file {} line {} ({})".format(
            self.msg, self.file, self.line, self.format
        )

class TestCtxtError(Exception):
    def __init__(self, msg, fil3, form4t):
        self.msg = msg
        self.file = fil3
        self.format = form4t

    def __str__(self):
        return "[TestCtxt] \"{}\" for file {} ({})".format(
            self.msg, self.file, self.format
        )

class ExecError(Exception):
    def __init__(self, msg, bin_name, test_name):
        self.msg = msg
        self.bin_name = bin_name
        self.test_name = test_name

    def __str__(self):
        return "[ExecExc] \"{}\" when running \"{}\" on \"{}\"".format(
            self.msg, self.bin_name, self.test_name
        )