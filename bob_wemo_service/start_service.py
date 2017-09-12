#!/usr/bin/python3
""" service_manager.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
from contextlib import suppress
import sys
if __name__ == "__main__":
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.wemo_service.configure import ConfigureService
from rpihome_v3.helpers.ref_num import RefNum
from rpihome_v3.helpers.message_handlers import MessageHandler
from rpihome_v3.wemo_service.wemo import WemoAPI
from rpihome_v3.wemo_service.service_main import MainTask


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Application wide objects ****************************************************
PARENT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_FILE = os.path.join(PARENT_PATH, 'config.ini')
SERVICE_CONFIG = ConfigureService(CONFIG_FILE)
LOG = SERVICE_CONFIG.get_logger()
SERVICE_ADDRESSES = SERVICE_CONFIG.get_servers()
MESSAGE_TYPES = SERVICE_CONFIG.get_message_types()
WEMO_GW = WemoAPI(LOG)

REF_NUM = RefNum(log=LOG)
LOOP = asyncio.get_event_loop()
COMM_HANDLER = MessageHandler(LOG, LOOP)
MAINTASK = MainTask(
    LOG,
    ref=REF_NUM,
    gw=WEMO_GW,
    msg_in_queue=COMM_HANDLER.msg_in_queue,
    msg_out_queue=COMM_HANDLER.msg_out_queue,
    service_addresses=SERVICE_ADDRESSES,
    message_types=MESSAGE_TYPES
)


# Main ************************************************************************
def main():
    """ Main application routine """
    LOG.debug('Starting main')

    # Create incoming message server
    try:
        LOG.debug('Creating incoming message listening server at [%s:%s]',
                  SERVICE_ADDRESSES['wemo_addr'],
                  SERVICE_ADDRESSES['wemo_port'])
        msg_in_server = asyncio.start_server(
            COMM_HANDLER.handle_msg_in,
            host=SERVICE_ADDRESSES['wemo_addr'],
            port=int(SERVICE_ADDRESSES['wemo_port']))
        LOG.debug('Wrapping servier in future task and scheduling for '
                  'execution')
        msg_in_task = LOOP.run_until_complete(msg_in_server)
    except Exception:
        LOG.debug('Failed to create socket listening connection at %s:%s',
                  SERVICE_ADDRESSES['wemo_addr'],
                  SERVICE_ADDRESSES['wemo_port'])
        sys.exit()

    # Create main task for this service
    LOG.debug('Scheduling main task for execution')
    asyncio.ensure_future(MAINTASK.run())

    # Create outgoing message task
    LOG.debug('Scheduling outgoing message task for execution')
    asyncio.ensure_future(COMM_HANDLER.handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    LOG.info('Wemo Gateway Service')
    LOG.info('Serving on {}'.format(msg_in_task.sockets[0].getsockname()))
    LOG.info('Press CTRL+C to exit')
    try:
        LOOP.run_forever()
    except asyncio.CancelledError:
        LOG.info('All tasks have been cancelled')
    except KeyboardInterrupt:
        pass
    finally:
        LOG.info('Shutting down incoming message server')
        msg_in_server.close()
        LOG.info('Finding all running tasks to shut down')
        pending = asyncio.Task.all_tasks()
        LOG.info('[%s] Task still running.  Closing them now', str(len(pending)))
        for i, task in enumerate(pending):
            with suppress(asyncio.CancelledError):
                LOG.info('Waiting for task [%s] to shut down', i)
                task.cancel()
                LOOP.run_until_complete(task)
        LOG.info('Shutdown complete.  Terminating execution LOOP')

    # Terminate the execution LOOP
    LOOP.close()


# Call Main *******************************************************************
if __name__ == "__main__":
    main()
