#!/usr/bin/python3
""" wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import pywemo
from bob_wemo_service.ipv4_help import check_ipv4


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The B.O.B. Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# pywemo wrapper API **********************************************************
class WemoAPI(object):
    """ Class and methods necessary to read items from a google calendar  """
    def __init__(self, logger):
        # Configure loggers
        self.logger = logger or logging.getLogger(__name__)
        # Configure other class objects
        self._wemo_known = []
        self.wemo_device = None
        self.wemo_port = None
        self.wemo_url = str()
        self.result = None
        self.status = str()
        self.logger.info('Performing initial scan for wemo devices on network')
        self._wemo_known = pywemo.discover_devices()
        for device in self._wemo_known:
            self.logger.info('Found: %s', device)


    @property
    def wemo_known(self):
        return self._wemo_known


    def search_by_name(self, name):
        self.logger.debug('Starting search of wemo table for matching name: %s', name)
        for i, d in enumerate(self._wemo_known):
            if name.lower() == d.name.lower():
                self.logger.debug('Match found at index: %s', i)
                return i
        self.logger.debug('No match found for device name: %s', name)
        return None


    def discover(self, name, address):
        """ discovers wemo device on network based upon known IP address """
        if check_ipv4(address) is True:
            self.logger.info(
                'Attempting to discover wemo device: %s @ %s',
                name, address
            )
            try:
                self.wemo_device = None
                self.wemo_port = pywemo.ouimeaux_device.probe_wemo(address)
                self.logger.debug('Device discovered at port %s', self.wemo_port)
            except Exception:
                self.wemo_port = None
                self.logger.warning('Failed to discover port for: %s', name)
        else:
            self.wemo_port = None
            self.logger.debug('Invalid IP address in device attributes')
        # If port was found, create url for device and run discovery function
        if self.wemo_port is not None:
            self.wemo_url = 'http://%s:%i/setup.xml' % (address, self.wemo_port)
            self.logger.debug('Resulting URL: %s', self.wemo_url)
            try:
                self.wemo_device = pywemo.discovery.device_from_description(
                    self.wemo_url,
                    None)
                self.logger.debug('Discovery successful for: %s', name)
                # Add newly discovered device to list of known devices
                self._wemo_known.append(copy.copy(self.wemo_device))
            except Exception:
                self.logger.warning('Discovery failed for: %s', name)
                self.wemo_device = None
        else:
            self.logger.warning('Discovery failed for: %s', name)
            self.wemo_device = None
        # Return device to calling program
        return self.wemo_device


    def read_status(self, name, address, status, last_seen):
        """ method to send a status query message to the physical device to
        request that it report its current status back to this program """
        self.logger.debug(
            'Querrying device status for: %s @ %s',
            name,
            address
        )
        # Check if device is already in the list of known wemo devices
        self.result = self.search_by_name(name)
        # Point to existing list record or recently discovered device
        if self.result is not None:
            self.wemo_device = self._wemo_known[self.result]
        else:
            self.wemo_device = self.discover(name, address)
        # Perform status query
        if self.wemo_device is not None:
            self.status = str(self.wemo_device.get_state(force_update=True))
            self.logger.debug(
                'Wemo device %s found with status: %s',
                name,
                self.status
            )
            # Update last seen timestamp
            last_seen = str(datetime.datetime.now())
        else:
            self.status = 'offline'
            self.logger.debug(
                'Wemo device %s discovery failed. Status set to: %s',
                name,
                self.status
            )
        # Return device status and timestamp
        return self.status, last_seen


    # Wemo set to on function *****************************************************
    def turn_on(self, name, address, last_seen):
        """ Send 'turn on' command to a specific wemo device """
        self.logger.debug(
            'Setting device state to "on" for: %s @ %s',
            name,
            address
        )
        # Check if device is already in the list of known wemo devices
        self.result = self.search_by_name(name)

        # Point to existing list record or recently discovered device
        if self.result is not None:
            self.wemo_device = self._wemo_known[self.result]
        else:
            self.logger.debug(
                'Device %s @ %s not previously discovered.  Running discovery',
                name,
                address
            )
            self.wemo_device = self.discover(name, address)

        # Perform command
        if self.wemo_device is not None:
            self.wemo_device.on()
            self.status = 'on'
            self.logger.debug(
                '"on" command sent to wemo device: %s',
                self.wemo_device.name
            )
            # Update last seen timestamp
            last_seen = str(datetime.datetime.now())
        else:
            self.status = 'offline'
            self.logger.debug(
                'Wemo device [%s] discovery failed.  Status set to: %s',
                name,
                self.status
            )
        # Return device status and timestamp
        return self.status, last_seen


    # Wemo set to off function ****************************************************
    def turn_off(self, name, address, last_seen):
        """ Send 'turn off' command to a specific wemo device """
        self.logger.debug(
            'Setting device state to "off" for: %s @ %s',
            name,
            address
        )
        # Check if device is already in the list of known wemo devices
        self.result = self.search_by_name(name)

        # Point to existing list record or recently discovered device
        if self.result is not None:
            self.wemo_device = self._wemo_known[self.result]
        else:
            self.logger.debug(
                'Device %s @ %s not previously discovered.  Running discovery',
                name,
                address
            )
            self.wemo_device = self.discover(name, address)

        # Perform command
        if self.wemo_device is not None:
            self.wemo_device.off()
            self.status = 'off'
            self.logger.debug(
                '"off" command sent to wemo device [%s]',
                self.wemo_device.name
            )
            # Update last seen timestamp
            last_seen = str(datetime.datetime.now())
        else:
            self.status = 'offline'
            self.logger.debug(
                'Wemo device [%s] discovery failed. Status set to [%s]',
                name,
                self.status
            )
        # Return device status and timestamp
        return self.status, last_seen
