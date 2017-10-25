#!/usr/bin/python3
""" test_dst.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import unittest
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bob_wemo_service.ref_num import RefNum


# Define test class ***********************************************************
class TestDst(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.ref_num = RefNum(logger=self.log)
        super(TestDst, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestDst, self).setUp()


    def test_init(self):
        self.assertEqual(self.ref_num.source, '100')


    def test_new(self):
        """ test class __init__ and input variables """
        self.assertEqual(self.ref_num.new(), '101')
        self.assertEqual(self.ref_num.new(), '102')
        self.assertEqual(self.ref_num.new(), '103')
        self.assertEqual(self.ref_num.new(), '104')
        self.ref_num.source = 998
        self.assertEqual(self.ref_num.source, '998')
        self.assertEqual(self.ref_num.new(), '999')
        self.assertEqual(self.ref_num.new(), '100')


if __name__ == "__main__":
    unittest.main()
