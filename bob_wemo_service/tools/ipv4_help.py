#!/usr/bin/python3
""" ipv4_help.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import re
import sys


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# IPv4 Format helper function *************************************************
def check_ipv4(address):
    """ simple function used to determine if the contents of a string are
    compatable with an ipv4 address """
    ipv4_regex = r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    # check if address is a string
    if isinstance(address, str) is not True:
        try:
            address = str(address)
        except Exception:
            return False
    # check if address is formatted correctly for an ipv4 address
    if re.fullmatch(ipv4_regex, address) is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)

    print("\n\nTesting check_ipv4 function")
    for i in range(250, 260, 1):
        addr = "192.168.1." + str(i)
        if check_ipv4(addr) is True:
            print(addr + " is valid")
        else:
            print(addr + " is not valid")
    print("\n\n")