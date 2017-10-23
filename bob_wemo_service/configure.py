#!/usr/bin/python3
""" configure.py:
    Configuration helper functions used to set up this service
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import logging
import logging.handlers
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bob_wemo_service.tools.device import Device


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Log Filter for Individual file/functions ************************************
class MyLogHandlerFilter(logging.Filter):
    def __init__(self, file_name, func_name):
        self.file_name = file_name
        self.func_name = func_name
        super().__init__()

    def filter(self, record):
        if len(self.file_name) != 0 and len(self.func_name) != 0:
            if record.filename == self.file_name and record.funcName == self.func_name:
                return True
            else:
                return False
        elif len(self.file_name) != 0 and len(self.func_name) == 0:
            if record.filename == self.file_name:
                return True
            else:
                return False
        elif len(self.file_name) == 0 and len(self.func_name) != 0:
            if record.funcName == self.func_name:
                return True
            else:
                return False
        elif len(self.file_name) == 0 and len(self.func_name) == 0:
            return True
        else:
            return False


# Config Function Def *********************************************************
class ConfigureService(object):
    def __init__(self, filename):
        self.filename = filename
        self.service_addresses = {}
        self.message_types = {}
        self.handlers = []
        self.filters = []
        self.formatters = []
        self.file_name = str()
        self.func_name = str()
        self.log_file_name = str()
        self.devices = []
        self.device_num = int()
        self.device_id = str()
        self.i = int()
        self.device = None
        self.name_key = str()
        self.type_key = str()
        self.addr_key = str()
        self.rule_key = str()
        # Define connection to configuration file
        self.config_file = configparser.ConfigParser()


    def get_logger(self):
        # Set up application logging
        self.config_file.read(self.filename)
        self.log_path = self.config_file['LOG FILES']['log_file_path']
        self.logger = logging.getLogger('master')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []
        os.makedirs(self.log_path, exist_ok=True)
        # Console handler
        self.ch = logging.StreamHandler(sys.stdout)
        self.ch.setLevel(logging.INFO)
        self.cf = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(self.cf)
        self.logger.addHandler(self.ch)
        self.logger.info('Console logger handler created and applied')
        # File handler
        self.fh = logging.handlers.TimedRotatingFileHandler(
            os.path.join(self.log_path, "Debug.log"),
            when='d',
            interval=1,
            backupCount=4
        )
        self.fh.setLevel(logging.DEBUG)
        self.ff = logging.Formatter(
            '%(asctime)-25s %(levelname)-10s '
            '%(funcName)-22s %(message)s'
        )
        self.fh.setFormatter(self.ff)
        self.logger.addHandler(self.fh)
        self.logger.info('File logger handler created and applied')

        # Extra handlers defined by config.ini
        self.i = 0
        for key, value in self.config_file.items('EXTRA LOG HANDLERS'):
            self.file_name = str()
            self.func_name = str()
            self.split = value.split("/", 1)
            if len(self.split) >= 1:
                self.file_name = self.split[0]
                self.log_file_name = self.split[0]
            if len(self.split) >= 2:
                self.func_name = self.split[1]
                if len(self.log_file_name) > 0:
                    self.log_file_name = self.log_file_name + "."
                self.log_file_name = self.log_file_name + self.split[1]
            self.log_file_name = self.log_file_name + ".log"

            # Create individual handler for this function name
            self.handlers.append(
                logging.handlers.TimedRotatingFileHandler(
                    os.path.join(self.log_path, self.log_file_name),
                    when='d',
                    interval=1,
                    backupCount=4
                )
            )
            # Create filter based on function name and apply to handler
            self.filters.append(
                MyLogHandlerFilter(
                    file_name=self.file_name,
                    func_name=self.func_name
                )
            )
            self.handlers[self.i].addFilter(self.filters[self.i])
            # Create formatter and apply to handler
            self.formatters.append(logging.Formatter('%(asctime)-25s %(levelname)-10s %(message)s'))
            self.handlers[self.i].setFormatter(self.formatters[self.i])
            # Add handler to logger
            self.logger.addHandler(self.handlers[self.i])
            self.i += 1

        # Return configured objects to main program
        return self.logger


    def get_servers(self):
        # Create dict with all services defined in INI file
        self.config_file.read(self.filename)
        for option in self.config_file.options('SERVICES'):
            self.service_addresses[option] = self.config_file['SERVICES'][option]
        # Return dict of configured addresses and ports to main program
        return self.service_addresses


    def get_message_types(self):
        # Create dict with all services defined in INI file
        self.config_file.read(self.filename)
        for option in self.config_file.options('MESSAGE TYPES'):
            self.message_types[option] = self.config_file['MESSAGE TYPES'][option]
        # Return dict of configured addresses and ports to main program
        return self.message_types


    def get_devices(self):
        self.config_file.read(self.filename)
        # Create list of automation devices defined in config.ini file
        self.devices = []
        self.logger.debug('Begining search for device configuration in config file')
        self.device_num = int(self.config_file['DEVICES']['device_num']) + 1
        self.logger.debug('Importing configuration for %s devices', str(self.device_num))
        for self.i in range(1, self.device_num, 1):
            try:
                if len(str(self.i)) == 1:
                    self.logger.debug('Single digit device ID number')
                    self.device_id = 'device0' + str(self.i)
                elif len(str(self.i)) == 2:
                    self.logger.debug('Double digit device ID number')
                    self.device_id = 'device' + str(self.i)
                self.logger.debug(
                    'Appending new %s to list',
                    self.device_id
                )
                self.name_key = self.device_id + '_name'
                self.type_key = self.device_id + '_devtype'
                self.addr_key = self.device_id + '_address'
                self.rule_key = self.device_id + '_rule'
                self.devices.append(
                    Device(
                        dev_name=self.config_file['DEVICES'][self.name_key],
                        dev_type=self.config_file['DEVICES'][self.type_key],
                        dev_addr=self.config_file['DEVICES'][self.addr_key],
                        dev_rule=self.config_file['DEVICES'][self.rule_key]
                    )
                )
                self.logger.debug(
                    'Device %s added to automation device list',
                    self.config_file['DEVICES'][self.name_key]
                )
            except Exception:
                self.logger.debug('error')
                pass
        self.logger.debug('Completed automation device list:')
        for self.device in self.devices:
            self.logger.debug(
                '%s, %s, %s, %s, %s, %s, %s',
                self.device.dev_name, self.device.dev_type,
                self.device.dev_addr, self.device.dev_cmd,
                self.device.dev_status, self.device.dev_last_seen,
                self.device.dev_rule)
        # Return configured objects to main program
        return self.devices
