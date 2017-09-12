#!/usr/bin/python3
""" logging.py: Log file setup helper functions
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import logging.handlers
import os
import sys


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Logging helper functions ****************************************************
def setup_log_handlers(name, debug_logfile, info_logfile):
    """ Function to configure root logger with three handlers, one to stream
    info and up messages, plus two additional file handlers for debug and info
    messages """
    root = logging.getLogger(name)
    root.setLevel(logging.DEBUG)
    root.handlers = []
    # Check if log files exist, create them if they don't
    os.makedirs(os.path.dirname(debug_logfile), exist_ok=True)
    os.makedirs(os.path.dirname(info_logfile), exist_ok=True)
    # Create desired handlers
    debug_handler = logging.handlers.TimedRotatingFileHandler(
        debug_logfile, when='d', interval=1, backupCount=7)
    info_handler = logging.handlers.TimedRotatingFileHandler(
        info_logfile, when='d', interval=1, backupCount=7)
    console_handler = logging.StreamHandler(sys.stdout)
    # Set logging levels for each handler
    debug_handler.setLevel(logging.DEBUG)
    info_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    # Create individual formats for each handler
    debug_formatter = logging.Formatter(
        '%(asctime)-25s %(levelname)-10s %(filename)-18s %(funcName)-22s %(message)s')
    info_formatter = logging.Formatter(
        '%(asctime)-25s %(levelname)-10s %(filename)-18s %(funcName)-22s %(message)s')
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    # Set formatting options for each handler
    debug_handler.setFormatter(debug_formatter)
    info_handler.setFormatter(info_formatter)
    console_handler.setFormatter(console_formatter)
    # Add handlers to root logger
    root.addHandler(debug_handler)
    root.addHandler(info_handler)
    root.addHandler(console_handler)
    root.debug("logging configured with 3 handlers")
    return root
