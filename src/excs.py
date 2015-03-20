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