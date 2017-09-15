#!/usr/bin/python3
""" wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import os
import sys
import pywemo
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bob_wemo_service.tools.log_support import setup_function_logger
from bob_wemo_service.tools.ipv4_help import check_ipv4


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# pywemo wrapper API **********************************************************
class WemoAPI(object):
    """ Class and methods necessary to read items from a google calendar  """
    def __init__(self, log_path):
        # Set up logging
        self.log_path = log_path
        self.log_init = setup_function_logger(self.log_path, 'Class_WemoAPI_Init')
        self.log_discover = setup_function_logger(self.log_path, 'Method_WemoAPI_discover')
        self.log_read_status = setup_function_logger(self.log_path, 'Method_WemoAPI_read_status')
        self.log_turn_on = setup_function_logger(self.log_path, 'Method_WemoAPI_turn_on')
        self.log_turn_off = setup_function_logger(self.log_path, 'Method_WemoAPI_turn_off')
        # Configure other class objects
        self.wemo_device = None
        self.wemo_port = None
        self.wemo_url = str()
        self.wemo_known = []
        self.result = None
        self.status = str()
        self.log_init.info('Performing initial scan for wemo devices on network')
        self.wemo_known = pywemo.discover_devices()
        for device in self.wemo_known:
            self.log_init.info('Found: %s', device)


    def discover(self, name, address):
        """ discovers wemo device on network based upon known IP address """
        if check_ipv4(address) is True:
            self.log_init.debug('Valid IP address provided')
            # Attempt to discover wemo device
            try:
                self.wemo_device = None
                self.wemo_port = pywemo.ouimeaux_device.probe_wemo(address)
                self.log_init.debug('Device discovered at port %s', self.wemo_port)
            except:
                self.wemo_port = None
                self.log_init.debug('Failed to discover port for [%s]', name)
        else:
            self.wemo_port = None
            self.log_init.debug('Invalid IP address in device attributes')
        # If port was found, create url for device and run discovery function
        if self.wemo_port is not None:
            self.wemo_url = 'http://%s:%i/setup.xml' % (address, self.wemo_port)
            self.log_init.debug('Resulting URL: [%s]', self.wemo_url)
            try:
                self.wemo_device = pywemo.discovery.device_from_description(
                    self.wemo_url,
                    None)
                self.log_init.debug('[%s] discovery successful', name)
            except:
                self.log_init.debug('[%s] discovery failed', name)
                self.wemo_device = None
        else:
            self.wemo_device = None
        # Return device to calling program
        return self.wemo_device


    def read_status(self, name, address, status, last_seen):
        """ method to send a status query message to the physical device to
        request that it report its current status back to this program """
        self.log_read_status.debug(
            'Querrying device [%s] at [%s], original status [%s / %s]',
            name,
            address,
            status,
            str(last_seen))
        # Check if device is already in the list of known wemo devices
        self.result = next(
            (index for index, wemodev in enumerate(self.wemo_known)
             if wemodev.name == name), None)
        # Point to existing list record or recently discovered device
        if self.result != None:
            self.wemo_device = self.wemo_known[self.result]
        else:
            self.wemo_device = self.discover(name, address)
        # Perform status query
        if self.wemo_device is not None:
            self.status = str(self.wemo_device.get_state(force_update=True))
            self.log_read_status.debug(
                'Wemo device [%s] found with status [%s]',
                name, self.status)
            # Re-define device record based on response from status query
            status = copy.copy(self.status)
            last_seen = datetime.datetime.now()
            # If device was not previously in wemo list, add it for next time
            if self.result is None:
                self.wemo_known.append(copy.copy(self.wemo_device))
            return self.status, str(datetime.datetime.now())
        else:
            self.status = 'offline'
            self.log_read_status.debug(
                'Wemo device [%s] discovery failed.  Status set to [%s]',
                name, self.status)
            status = copy.copy(self.status)
            return self.status, last_seen


    # Wemo set to on function *****************************************************
    def turn_on(self, name, address, status, last_seen):
        """ Send 'turn on' command to a specific wemo device """
        self.log_turn_on.debug('Setting device [%s] at [%s], state to "on"',
            name, address)
        # Check if device is already in the list of known wemo devices
        self.result = next(
            (index for index, wemodev in enumerate(self.wemo_known)
             if wemodev.name == name), None)
        # Point to existing list record or recently discovered device
        if self.result == None:
            self.log_turn_on.debug('Device not in wemo list.  Running discovery')
            self.wemo_device = self.discover(name, address)
        else:
            self.log_turn_on.debug('Device already in wemo list as [%s]',
                self.wemo_known[self.result])
            self.wemo_device = self.wemo_known[self.result]
        # Perform command, followed by status query
        if self.wemo_device is not None:
            self.wemo_device.on()
            self.status = 'on'
            self.log_turn_on.debug('"on" command sent to wemo device [%s]',
                           self.wemo_device.name)
            last_seen = str(datetime.datetime.now())
            # If device was not previously in wemo list, add it for next time
            if self.result == None:
                self.wemo_known.append(copy.copy(self.wemo_device))
        else:
            self.status = 'offline'
            self.log_turn_on.debug('Wemo device [%s] discovery failed.  Status set to [%s]',
                name, self.status)
        return self.status, last_seen


    # Wemo set to off function ****************************************************
    def turn_off(self, name, address, status, last_seen):
        """ Send 'turn off' command to a specific wemo device """
        self.log_turn_off.debug(
            'Setting device [%s] at [%s], state to "off"',
            name,
            address)
        # Check if device is already in the list of known wemo devices
        self.result = next(
            (index for index, wemodev in enumerate(self.wemo_known)
             if wemodev.name == name), None)
        # Point to existing list record or recently discovered device
        if self.result == None:
            self.log_turn_off.debug('Device not in wemo list.  Running discovery')
            self.wemo_device = self.discover(name, address)
        else:
            self.log_turn_off.debug(
                'Device already in wemo list as [%s]',
                self.wemo_known[self.result])
            self.wemo_device = self.wemo_known[self.result]
        # Perform command, followed by status query
        if self.wemo_device is not None:
            self.wemo_device.off()
            self.status = 'off'
            self.log_turn_off.debug(
                '"off" command sent to wemo device [%s]', self.wemo_device.name)
            # Re-define device record based on response from status query
            last_seen = str(datetime.datetime.now())
            # If device was not previously in wemo list, add it for next time
            if self.result == None:
                self.wemo_known.append(copy.copy(self.wemo_device))
        else:
            self.status = 'offline'
            self.log_turn_off.debug('Wemo device [%s] discovery failed.  Status set to [%s]',
                name, self.status)
        return self.status, last_seen
