#!/usr/bin/python3
""" ref_num.py: Message reference number class
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import sys


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class definition ************************************************************
class RefNum(object):
    def __init__(self, log):
        # Configure logger
        self.log = log or logging.getLogger(__name__)
        # Init tags
        self._source = 100

    # source control **********************************************************
    @property
    def source(self):
        self.log.debug('Returning current value: %s', self._source)
        return str(self._source)

    @source.setter
    def source(self, value):
        if isinstance(value, int):
            self._source = value
            self.log.debug('Source updated to: %s', self._source)
        elif isinstance(value, str):
            self._source = int(value)
            self.log.debug('Source updated to: %s', self._source)
        else:
            self.log.debug('Invalid source value: %s', value)

    # new value control *******************************************************
    def new(self):
        self._source += 1
        if self._source > 999:
            self._source = 100
        return str(self._source)


if __name__ == "__main__":
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)

    rn = RefNum(root)
    print("\n\nTesting RefNum class")
    for i in range(1, 10, 1):
        print(rn.new())
    print("\n\n")
