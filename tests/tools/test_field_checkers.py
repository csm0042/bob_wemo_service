#!/usr/bin/python3
""" test_message_ccs.py:
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
from bob_wemo_service.tools.field_checkers import in_int_range
from bob_wemo_service.tools.field_checkers import is_valid_datetime


# Define test class ***********************************************************
class TestFieldCheckers(unittest.TestCase):
    """ unittests for field checkers for messages """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG

        self.dt_initial = datetime.datetime
        self.dt_test_input = datetime.datetime
        self.dt_check = datetime.datetime

        super(TestFieldCheckers, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestFieldCheckers, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_in_int_range(self):
        """ test function which checks whether an input value is within a
            range of integers """
        self.assertEqual(in_int_range(self.log, 202, 100, 999), True)
        self.assertEqual(in_int_range(self.log, 202, 1000, 9999), False)
        self.assertEqual(in_int_range(self.log, -1, 0, 999), False)
        self.assertEqual(in_int_range(self.log, 202, 100, 199), False)


    def test_is_valid_datetime1(self):
        """ test Valid input (datetime) and valid initial (datetime) value """
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_test_input = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_check = str(datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0))
        )[:19]

        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime2(self):
        """ test Valid input (datetime.date) and valid initial (datetime) value """
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_test_input = datetime.date(2017, 2, 1)
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 2, 1), datetime.time(9, 3, 0))
            )[:10]

        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            )[0:10],
            self.dt_check
        )

    def test_is_valid_datetime3(self):
        """ test Valid input (datetime.time) and valid initial (datetime) value """
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_test_input = datetime.time(10, 12, 1)
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.datetime.now().date(), datetime.time(10, 12, 1))
            )[:19]

        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime4(self):
        """ test Valid input (datetime string) and valid initial (datetime) value """
        
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_test_input = '2017-01-01 09:03:00'
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 1, 1), datetime.time(9, 3, 0))
            )[:19]

        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
        self.dt_check
        )

    def test_is_valid_datetime5(self):
        """ test Valid input (datetime.date string) and valid initial (datetime) value """
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_test_input = '2017-02-01'
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 2, 1), datetime.time(9, 3, 0))
            )[:10]
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            )[0:10],
            self.dt_check
        )

    def test_is_valid_datetime6(self):
        """ test Valid input (datetime.time string) and valid initial (datetime) value """
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_test_input = '10:12:01'        
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.datetime.now().date(), datetime.time(10, 12, 1))
            )[:19]
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime7(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-13-01 09:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 1, 1), datetime.time(9, 4, 0))
            )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime8(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-12-32 09:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 1, 1), datetime.time(9, 4, 0))
            )   
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime9(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-12-31 24:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 1, 1), datetime.time(9, 4, 0))
            )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime10(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-12-31 23:60:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 1, 1), datetime.time(9, 4, 0))
            )[:19]
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime11(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-12-31 23:59:60'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 1, 1), datetime.time(9, 4, 0))
            )[:19]        
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime12(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-12-31 23:59:59'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 12, 31), datetime.time(23, 59, 59))
            )[:19]        
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )

    def test_is_valid_datetime13(self):
        """ test various invalid datetime.datetime string formats """
        self.dt_test_input = '2017-12-31 00:00:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.dt_check = str(
            datetime.datetime.combine(
                datetime.date(2017, 12, 31), datetime.time(0, 0, 0))
            )[:19]        
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt_test_input,
                self.dt_initial
            ),
            self.dt_check
        )



if __name__ == "__main__":
    unittest.main()
