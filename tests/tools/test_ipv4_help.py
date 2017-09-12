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
from bob_wemo_service.tools.ipv4_help import check_ipv4


# Define test class ***********************************************************
class TestDst(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        super(TestDst, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestDst, self).setUp()


    def test_check_ipv4(self):
        """ test class __init__ and input variables """
        self.assertEqual(check_ipv4('192.168.4.4'), True)
        self.assertEqual(check_ipv4('192.168.x.4'), False)
        self.assertEqual(check_ipv4('1.1.4.4'), True)
        self.assertEqual(check_ipv4('127.0.0.1'), True)





if __name__ == "__main__":
    unittest.main()
