#!/usr/bin/python3
""" ref_num.py: Message reference number class
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The B.O.B. Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class definition ************************************************************
class RefNum(object):
    def __init__(self, logger=None):
        # Configure loggers
        self.logger = logger or logging.getLogger(__name__)

        # Init tags
        self.logger.debug('Setting source register to initial value of 100')
        self._source = 100

    # source control **********************************************************
    @property
    def source(self):
        self.logger.debug('Returning current value: %s', self._source)
        return str(self._source)

    @source.setter
    def source(self, value):
        if isinstance(value, int):
            self._source = value
            self.logger.debug('Source updated to: %s', self._source)
        elif isinstance(value, str):
            self._source = int(value)
            self.logger.debug('Source updated to: %s', self._source)
        else:
            self.logger.debug('Invalid source value: %s', value)

    # new value control *******************************************************
    def new(self):
        self.logger.debug('Incrementing source register')
        self._source += 1
        if self._source > 999:
            self.logger.debug('Rolling over source register')
            self._source = 100
        self.logger.debug('Returning source value to main: %d', self._source)
        return str(self._source)
