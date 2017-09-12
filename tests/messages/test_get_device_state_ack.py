#!/usr/bin/python3
""" test_message_gds_ack.py:
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
from bob_wemo_service.messages.get_device_state_ack import GetDeviceStateMessageACK


# Define test class ***********************************************************
class TestGetDeviceStateMessageACK(unittest.TestCase):
    """ unittests for Log Status Update Message Class """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.datetime = datetime.datetime
        self.datetime_str = str()
        self.temp_str = str()
        self.temp_str2 = str()
        super(TestGetDeviceStateMessageACK, self).__init__(*args, **kwargs)


    def setUp(self):
        self.message = GetDeviceStateMessageACK(log=self.log)
        super(TestGetDeviceStateMessageACK, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        self.datetime = datetime.datetime.now()
        self.datetime_str = (str(self.datetime))[:19]
        self.message = GetDeviceStateMessageACK(
            log=self.log,
            ref='101',
            dest_addr='192.168.86.1',
            dest_port='17061',
            source_addr='192.168.5.4',
            source_port='12000',
            msg_type='601',
            dev_name='fylt1',
            dev_status='on',
            dev_last_seen=self.datetime
        )
        self.assertEqual(self.message.ref, '101')
        self.assertEqual(self.message.dest_addr, '192.168.86.1')
        self.assertEqual(self.message.dest_port, '17061')
        self.assertEqual(self.message.source_addr, '192.168.5.4')
        self.assertEqual(self.message.source_port, '12000')
        self.assertEqual(self.message.msg_type, '601')
        self.assertEqual(self.message.dev_name, 'fylt1')
        self.assertEqual(self.message.dev_status, 'on')
        self.assertEqual(self.message.dev_last_seen, self.datetime_str)


    def test_ref_number(self):
        """ test setting and getting message reference number field """
        self.message.ref = 100
        self.assertEqual(self.message.ref, '100')
        self.message.ref = '202'
        self.assertEqual(self.message.ref, '202')


    def test_dest_addr(self):
        """ test setting and getting message destination address field """
        self.message.dest_addr = '192.168.1.1'
        self.assertEqual(self.message.dest_addr, '192.168.1.1')
        self.message.dest_addr = '192.168.2.x'
        self.assertEqual(self.message.dest_addr, '192.168.1.1')


    def test_dest_port(self):
        """ test setting and getting message destination port field """
        self.message.dest_port = 11000
        self.assertEqual(self.message.dest_port, '11000')
        self.message.dest_port = '12000'
        self.assertEqual(self.message.dest_port, '12000')
        self.message.dest_port = 100
        self.assertEqual(self.message.dest_port, '12000')
        self.message.dest_port = '101'
        self.assertEqual(self.message.dest_port, '12000')
        self.message.dest_port = '100000'
        self.assertEqual(self.message.dest_port, '12000')
        self.message.dest_port = 101000
        self.assertEqual(self.message.dest_port, '12000')
        self.message.dest_port = 17061
        self.assertEqual(self.message.dest_port, '17061')
        self.message.dest_port = '?'
        self.assertEqual(self.message.dest_port, '17061')
        self.message.dest_port = 'a'
        self.assertEqual(self.message.dest_port, '17061')


    def test_source_addr(self):
        """ test setting and getting message source address field """
        self.message.source_addr = '192.168.1.1'
        self.assertEqual(self.message.source_addr, '192.168.1.1')
        self.message.source_addr = '192.168.2.x'
        self.assertEqual(self.message.source_addr, '192.168.1.1')


    def test_source_port(self):
        """ test setting and getting message source port field """
        self.message.source_port = 11000
        self.assertEqual(self.message.source_port, '11000')
        self.message.source_port = '12000'
        self.assertEqual(self.message.source_port, '12000')
        self.message.source_port = 100
        self.assertEqual(self.message.source_port, '12000')
        self.message.source_port = '101'
        self.assertEqual(self.message.source_port, '12000')
        self.message.source_port = '100000'
        self.assertEqual(self.message.source_port, '12000')
        self.message.source_port = 101000
        self.assertEqual(self.message.source_port, '12000')
        self.message.source_port = 17061
        self.assertEqual(self.message.source_port, '17061')
        self.message.source_port = '?'
        self.assertEqual(self.message.source_port, '17061')
        self.message.source_port = 'a'
        self.assertEqual(self.message.source_port, '17061')           


    def test_message_type(self):
        """ test setting and getting message type field """
        self.message.msg_type = 101
        self.assertEqual(self.message.msg_type, '101')
        self.message.msg_type = '102'
        self.assertEqual(self.message.msg_type, '102')


    def test_device_name(self):
        """ test setting and getting device name field """
        self.message.dev_name = 101
        self.assertEqual(self.message.dev_name, '101')
        self.message.dev_name = 'fylt1'
        self.assertEqual(self.message.dev_name, 'fylt1')


    def test_dev_status(self):
        """ test setting and getting device status field """
        self.message.dev_status = 'off'
        self.assertEqual(self.message.dev_status, 'off')
        self.message.dev_status = '1'
        self.assertEqual(self.message.dev_status, '1')


    def test_dev_last_seen(self):
        """ test setting and getting device status field """
        self.datetime = datetime.datetime.combine(
            datetime.date(2017, 10, 3),
            datetime.time(7, 30))
        self.datetime_str = (str(self.datetime))[:19]
        self.message.dev_last_seen = self.datetime
        self.assertEqual(self.message.dev_last_seen, self.datetime_str)      


    def test_complete(self):
        self.temp_str = '142,127.0.0.1,12000,192.168.5.45,13000,301,device01,on,2017-10-04 07:01:03.000034'
        self.temp_str2 = '142,127.0.0.1,12000,192.168.5.45,13000,301,device01,on,2017-10-04 07:01:03'
        self.message.complete = copy.copy(self.temp_str)
        self.assertEqual(self.message.ref, '142')
        self.assertEqual(self.message.dest_addr, '127.0.0.1')
        self.assertEqual(self.message.dest_port, '12000')
        self.assertEqual(self.message.source_addr, '192.168.5.45')
        self.assertEqual(self.message.source_port, '13000')
        self.assertEqual(self.message.msg_type, '301')
        self.assertEqual(self.message.dev_name, 'device01')
        self.assertEqual(self.message.dev_status, 'on')
        self.assertEqual(self.message.dev_last_seen, '2017-10-04 07:01:03')
        self.assertEqual(self.message.complete, self.temp_str2)

        self.temp_str = '142,192.168.1,12000,192.168.5.45,130000,301,device01,on,2017-10-04 07:01:04'
        self.temp_str2 = '142,127.0.0.1,12000,192.168.5.45,13000,301,device01,on,2017-10-04 07:01:04'
        self.message.complete = copy.copy(self.temp_str)
        self.assertEqual(self.message.ref, '142')
        self.assertEqual(self.message.dest_addr, '127.0.0.1')
        self.assertEqual(self.message.dest_port, '12000')
        self.assertEqual(self.message.source_addr, '192.168.5.45')
        self.assertEqual(self.message.source_port, '13000')
        self.assertEqual(self.message.msg_type, '301')
        self.assertEqual(self.message.dev_name, 'device01')
        self.assertEqual(self.message.dev_status, 'on')
        self.assertEqual(self.message.dev_last_seen, '2017-10-04 07:01:04')        
        self.assertEqual(self.message.complete, self.temp_str2)

        self.temp_str = '142,192.168.1.1,12001,192.168.5.46,13001,301,device01,off,2017-10-04 07:01:04'
        self.temp_str2 = '142,192.168.1.1,12001,192.168.5.46,13001,301,device01,off,2017-10-04 07:01:04'
        self.message.complete = copy.copy(self.temp_str)
        self.assertEqual(self.message.ref, '142')
        self.assertEqual(self.message.dest_addr, '192.168.1.1')
        self.assertEqual(self.message.dest_port, '12001')
        self.assertEqual(self.message.source_addr, '192.168.5.46')
        self.assertEqual(self.message.source_port, '13001')
        self.assertEqual(self.message.msg_type, '301')
        self.assertEqual(self.message.dev_name, 'device01')
        self.assertEqual(self.message.dev_status, 'off')
        self.assertEqual(self.message.dev_last_seen, '2017-10-04 07:01:04')        
        self.assertEqual(self.message.complete, self.temp_str2)


if __name__ == "__main__":
    unittest.main()
