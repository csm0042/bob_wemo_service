#!/usr/bin/python3
""" test_logger.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import unittest
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bob_wemo_service.tools.log_support import setup_log_handlers


# Define test class ***********************************************************
class TestLogger(unittest.TestCase):
    """ unittests for logger.py """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.info_file = "c://python_logs//info.log"
        self.debug_file = "c://python_logs//debug.log"
        self.logger = setup_log_handlers(
            __file__, self.debug_file, self.info_file)
        super(TestLogger, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestLogger, self).setUp()


    def test_setup_log_handlers(self):
        """ tests to see if the correct number of log handlers
        have been created """
        self.assertEqual(len(self.logger.handlers), 3)


if __name__ == "__main__":
    unittest.main()
    