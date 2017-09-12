#!/usr/bin/python3
""" start.py:
    Master start routine for the RpiHome application.  Starts each service in
    a separate shell in an order that prevents loss of data between services
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import os


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Startup Window Mode *********************************************************
minimize = True
maximize = False
if minimize is True:
    mode = '/MIN'
elif maximize is True:
    mode = '/MAX'
else:
    mode = ''

# Open command windows and start individual services **************************
os.system('start "RpiHome Database Service" %s /D "C://Users//chris.maue//OneDrive//Git//rpihome_v3//rpihome_v3//database_service" python start_service.py"' % mode)
os.system('start "RpiHome WEMO Service" %s /D "C://Users//chris.maue//OneDrive//Git//rpihome_v3//rpihome_v3//wemo_service" python start_service.py"' % mode)
os.system('start "RpiHome Automation Service" %s /D "C://Users//chris.maue//OneDrive//Git//rpihome_v3//rpihome_v3//automation_service" python start_service.py"' % mode)
os.system('start "RpiHome Schedule Service" %s /D "C://Users//chris.maue//OneDrive//Git//rpihome_v3//rpihome_v3//schedule_service" python start_service.py"' % mode)
