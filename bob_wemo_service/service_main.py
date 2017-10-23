#!/usr/bin/python3
""" wemo_service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import logging
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bob_wemo_service.msg_processing import create_heartbeat_msg
from bob_wemo_service.msg_processing import process_heartbeat_msg
from bob_wemo_service.msg_processing import get_wemo_state
from bob_wemo_service.msg_processing import set_wemo_state



# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Internal Service Work Task **************************************************
class MainTask(object):
    def __init__(self, logger, **kwargs):
        # Configure loggers
        self.logger = logger or logging.getLogger(__name__)
        # Define instance variables
        self.ref_num = None
        self.gateway = None
        self.msg_in_queue = None
        self.msg_out_queue = None
        self.service_addresses = []
        self.message_types = []
        self.last_check_hb = datetime.datetime.now()
        self.sleep_time = 0.2
        self.out_msg = str()
        self.out_msg_list = []
        self.next_msg = str()
        self.next_msg_split = []
        self.msg_source_addr = str()
        self.msg_source_port = str()
        self.msg_type = str()
        self.destinations = []
        self.match = False
        self.device = None
        self.devices = []
        self.wemo_device = None
        self.discover_wemo_ts = datetime.datetime
        # Map input variables
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "ref":
                    self.ref_num = value
                    self.logger.debug('Ref number generator set during __init__ '
                                      'to: %s', self.ref_num)
                if key == "gw":
                    self.gateway = value
                    self.logger.debug('Device gateway set during __init__ '
                                      'to: %s', self.gateway)
                if key == "msg_in_queue":
                    self.msg_in_queue = value
                    self.logger.debug('Message in queue set during __init__ '
                                      'to: %s', self.msg_in_queue)
                if key == "msg_out_queue":
                    self.msg_out_queue = value
                    self.logger.debug('Message out queue set during __init__ '
                                      'to: %s', self.msg_out_queue)
                if key == "service_addresses":
                    self.service_addresses = value
                    self.logger.debug('Service address list set during __init__ '
                                      'to: %s', self.service_addresses)
                if key == "message_types":
                    self.message_types = value
                    self.logger.debug('Message type list set during __init__ '
                                      'to: %s', self.message_types)
                if key == "devices":
                    self.devices = value
                    self.logger.debug('Device list set during __init__ '
                                      'to: %s', self.devices)


    def discover_wemo(self):
        # Search Network for any devices not previously discovered
        self.logger.debug(
            'Checking list of discovered devices against configured '
            'device list: %s', self.devices
        )
        for self.device in self.devices:
            if 'wemo' in self.device.dev_type:
                self.match = False
                for self.wemo_device in self.gateway.wemo_known:
                    if self.device.dev_name == self.wemo_device.name:
                        self.match = True
                        self.logger.debug(
                            'Device %s already discovered',
                            self.device.dev_name
                        )
                        break
                if self.match is False:
                    self.logger.debug(
                        'Device %s not previously discovered. Running discovery now',
                        self.device.dev_name
                    )
                    self.gateway.discover(
                        self.device.dev_name,
                        self.device.dev_addr
                    )


    @asyncio.coroutine
    def run(self):
        """ task to handle the work the service is intended to do """
        self.logger.info('Starting wemo service main task')

        # Search Network for any devices not previously discovered
        self.discover_wemo()
        self.discover_wemo_ts = datetime.datetime.now()

        # Main process loop
        while True:
            # Initialize result list
            self.out_msg_list = []
            self.sleep_time = 0.2

            # INCOMING MESSAGE HANDLING
            if self.msg_in_queue.qsize() > 0:
                self.sleep_time = 0.01
                self.logger.debug('Getting Incoming message from queue')
                self.next_msg = self.msg_in_queue.get_nowait()
                self.logger.debug('Message pulled from queue: [%s]', self.next_msg)

                # Determine message type
                self.next_msg_split = self.next_msg.split(',')
                if len(self.next_msg_split) >= 6:
                    self.logger.debug('Extracting source address and message type')
                    self.msg_source_addr = self.next_msg_split[3]
                    self.msg_source_port = self.next_msg_split[4]
                    self.msg_type = self.next_msg_split[5]
                    self.logger.debug('Source Address: %s', self.msg_source_addr)
                    self.logger.debug('Source Port: %s', self.msg_source_addr)
                    self.logger.debug('Message Type: %s', self.msg_type)

                # Process heartbeat from remote service
                if self.msg_type == self.message_types['heartbeat']:
                    self.logger.debug('Message is a heartbeat')
                    self.out_msg_list = process_heartbeat_msg(
                        self.logger,
                        self.ref_num,
                        self.next_msg,
                        self.message_types)

                # Wemo Device Status Queries
                if self.msg_type == self.message_types['get_device_state']:
                    self.logger.debug('Message is a device status update request')
                    self.out_msg_list = yield from get_wemo_state(
                        self.logger,
                        self.ref_num,
                        self.gateway,
                        self.next_msg,
                        self.message_types)

                # Wemo Device set state commands
                if self.msg_type == self.message_types['set_device_state']:
                    self.logger.debug('Message is a device set state command')
                    self.out_msg_list = yield from set_wemo_state(
                        self.logger,
                        self.ref_num,
                        self.gateway,
                        self.next_msg,
                        self.message_types)

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.logger.debug('Queueing response message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(copy.copy(self.out_msg))
                        self.logger.debug('Message [%s] successfully queued', self.out_msg)


            # PERIODIC TASKS
            # Periodically send heartbeats to other services
            if datetime.datetime.now() >= (self.last_check_hb + datetime.timedelta(seconds=60)):
                self.destinations = [
                    (self.service_addresses['automation_addr'],
                     self.service_addresses['automation_port'])
                ]
                self.out_msg_list = create_heartbeat_msg(
                    self.logger,
                    self.ref_num,
                    self.destinations,
                    self.service_addresses['wemo_addr'],
                    self.service_addresses['wemo_port'],
                    self.message_types)

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.logger.debug('Queueing response message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(copy.copy(self.out_msg))
                        self.logger.debug('Response message [%s] successfully queued',
                                          self.out_msg)

                # Update last-check
                self.last_check_hb = datetime.datetime.now()


            # WEMO DEVICE DISCOVERY
            # Search Network for any devices not previously discovered
            if datetime.datetime.now() >= (self.discover_wemo_ts + datetime.timedelta(minutes=5)):
                self.discover_wemo()
                self.discover_wemo_ts = datetime.datetime.now()


            # Yield to other tasks for a while
            yield from asyncio.sleep(self.sleep_time)
