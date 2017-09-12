#!/usr/bin/python3
""" start.py:
    Master start routine for the RpiHome application.  Starts each service in
    a separate shell in an order that prevents loss of data between services
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from bob_wemo_service.start_service import main as start_service


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


if __name__ == "__main__":
    start_service()
