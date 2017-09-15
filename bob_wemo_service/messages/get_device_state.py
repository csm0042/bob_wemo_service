#!/usr/bin/python3
""" message_gds.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bob_wemo_service.tools.log_support import setup_function_logger
from bob_wemo_service.tools.ipv4_help import check_ipv4
from bob_wemo_service.tools.field_checkers import in_int_range
from bob_wemo_service.tools.field_checkers import is_valid_datetime


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Message Class Definition ****************************************************
class GetDeviceStateMessage(object):
    """ Log Status Update message class and methods """
    def __init__(self, log_path, **kwargs):
        # Configure loggers
        self.log_path = log_path
        self.log = setup_function_logger(self.log_path, 'Class_GetDeviceStateMessage')

        self._ref = str()
        self._dest_addr = str()
        self._dest_port = str()
        self._source_addr = str()
        self._source_port = str()
        self._msg_type = str()
        self._dev_name = str()
        self._dev_addr = str()
        self._dev_status = str()
        self._dev_last_seen = str()
        self.temp_list = []
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "ref":
                    self.ref = value
                    self.log.debug('Ref Number value set during '
                                   '__init__ to: %s', self.ref)
                if key == "dest_addr":
                    self.dest_addr = value
                    self.log.debug('Destination address value set during __init__ '
                                   'to: %s', self.dest_addr)
                if key == "dest_port":
                    self.dest_port = value
                    self.log.debug('Destination port value set during __init__ '
                                   'to: %s', self.dest_port)
                if key == "source_addr":
                    self.source_addr = value
                    self.log.debug('Source address value set during __init__ '
                                   'to: %s', self.source_addr)
                if key == "source_port":
                    self.source_port = value
                    self.log.debug('Source port value set during __init__ to: '
                                   '%s', self.source_port)
                if key == "msg_type":
                    self.msg_type = value
                    self.log.debug('Message type value set during __init__ to: '
                                   '%s', self.msg_type)
                if key == "dev_name":
                    self.dev_name = value
                    self.log.debug('Device name value set during __init__ to: '
                                   '%s', self.dev_name)
                if key == "dev_addr":
                    self.dev_addr = value
                    self.log.debug('Device Address value set during __init__ '
                                   'to: %s', self.dev_addr)
                if key == "dev_status":
                    self.dev_status = value
                    self.log.debug('Device Status value set during __init__ '
                                   'to: %s', self.dev_status)                                   
                if key == "dev_last_seen":
                    self.dev_last_seen = value
                    self.log.debug('Device last seen value set during __init__ '
                                   'to: %s', self.dev_last_seen)

    # ref number field ********************************************************
    @property
    def ref(self):
        self.log.debug('Returning current value of ref number: %s', self._ref)
        return self._ref

    @ref.setter
    def ref(self, value):
        if in_int_range(self.log_path, value, 100, 999) is True:
            self._ref = str(value)
            self.log.debug('Ref number updated to: %s', self._ref)
        else:
            self.log.debug('Ref number update failed with input value: '
                           '%s', value)

    # destination address *****************************************************
    @property
    def dest_addr(self):
        self.log.debug('Returning current value of destination address: '
                       '%s', self._dest_addr)
        return self._dest_addr

    @dest_addr.setter
    def dest_addr(self, value):
        if check_ipv4(value) is True:
            self._dest_addr = str(value)
            self.log.debug('Destination address updated to: '
                            '%s', self._dest_addr)
        else:
            self.log.warning('Destination address update failed with input value: '
                             '%s', value)

    # destination port ********************************************************
    @property
    def dest_port(self):
        self.log.debug('Returning current value of destination port: '
                       '%s', self._dest_port)
        return self._dest_port

    @dest_port.setter
    def dest_port(self, value):
        if in_int_range(self.log_path, value, 10000, 60000) is True:
            self._dest_port = str(value)
            self.log.debug('Destination port updated to: %s', self._dest_port)
        else:
            self.log.debug('Destination port update failed with input value: '
                           '%s', value)

    # source address field ****************************************************
    @property
    def source_addr(self):
        self.log.debug('Returning current value of source address: '
                       '%s', self._source_addr)
        return self._source_addr

    @source_addr.setter
    def source_addr(self, value):
        if check_ipv4(value) is True:
            self._source_addr = value
            self.log.debug('source address updated to: '
                           '%s', self._source_addr)
        else:
            self.log.warning('Source address update failed with input value: '
                             '%s', value)

    # source port field *******************************************************
    @property
    def source_port(self):
        self.log.debug('Returning current value of source port: '
                       '%s', self._source_port)
        return self._source_port

    @source_port.setter
    def source_port(self, value):
        if in_int_range(self.log_path, value, 10000, 60000) is True:
            self._source_port = str(value)
            self.log.debug('Source port updated to: %s', self._source_port)
        else:
            self.log.debug('Source port update failed with input value: '
                           '%s', value)

    # message type field ******************************************************
    @property
    def msg_type(self):
        self.log.debug('Returning current value of message type: '
                       '%s', self._msg_type)
        return self._msg_type

    @msg_type.setter
    def msg_type(self, value):
        if in_int_range(self.log_path, value, 100, 999) is True:
            self._msg_type = str(value)
            self.log.debug('Message type updated to: %s', self._msg_type)
        else:
            self.log.debug('Message type update failed with input value: '
                           '%s', value)

    # device name field *******************************************************
    @property
    def dev_name(self):
        self.log.debug('Returning current value of device name: '
                       '%s', self._dev_name)
        return self._dev_name

    @dev_name.setter
    def dev_name(self, value):
        if isinstance(value, str):
            self._dev_name = value
        else:
            self._dev_name = str(value)
        self.log.debug('Device name value updated to: '
                       '%s', self._dev_name)

    # device address field ****************************************************
    @property
    def dev_addr(self):
        self.log.debug('Returning current value of device address: '
                       '%s', self._dev_addr)
        return self._dev_addr

    @dev_addr.setter
    def dev_addr(self, value):
        if check_ipv4(value) is True:
            self._dev_addr = value
            self.log.debug('Device address updated to: '
                           '%s', self._dev_addr)
        else:
            self.log.warning('Device address update failed with input value: '
                             '%s', value)

    # device status field *****************************************************
    @property
    def dev_status(self):
        self.log.debug('Returning current value of device status: '
                       '%s', self._dev_status)
        return self._dev_status

    @dev_status.setter
    def dev_status(self, value):
        if isinstance(value, str):
            self._dev_status = value.lower()
        else:
            self._dev_status = (str(value)).lower()
        self.log.debug('Device status value updated to: '
                       '%s', self._dev_status)

    # device last seen field **************************************************
    @property
    def dev_last_seen(self):
        self.log.debug('Returning current value of device last seen: '
                       '%s', self._dev_last_seen)
        return self._dev_last_seen

    @dev_last_seen.setter
    def dev_last_seen(self, value):
        self._dev_last_seen = is_valid_datetime(
            self.log,
            value,
            self._dev_last_seen)
        self.log.debug('Device last seen updated to: %s', self._dev_last_seen)

    # complete message encode/decode methods **********************************
    @property
    def complete(self):
        self.log.debug('Returning current value of complete message: '
                       '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s',
                       self._ref, self._dest_addr, self._dest_port,
                       self._source_addr, self._source_port,
                       self._msg_type, self._dev_name, self._dev_addr,
                       self._dev_status, self._dev_last_seen)
        return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
            self._ref, self._dest_addr, self._dest_port,
            self._source_addr, self._source_port,
            self._msg_type, self._dev_name, self._dev_addr,
            self._dev_status, self._dev_last_seen)

    @complete.setter
    def complete(self, value):
        if isinstance(value, str):
            self.temp_list = value.split(',')
            if len(self.temp_list) >= 10:
                self.log.debug('Message was properly formatted for decoding')
                self.ref = self.temp_list[0]
                self.dest_addr = self.temp_list[1]
                self.dest_port = self.temp_list[2]
                self.source_addr = self.temp_list[3]
                self.source_port = self.temp_list[4]
                self.msg_type = self.temp_list[5]
                self.dev_name = self.temp_list[6]
                self.dev_addr = self.temp_list[7]
                self.dev_status = self.temp_list[8]
                self.dev_last_seen = self.temp_list[9]
