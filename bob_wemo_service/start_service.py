#!/usr/bin/python3
""" service_manager.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
from contextlib import suppress
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bob_wemo_service.tools.log_support import setup_function_logger
from bob_wemo_service.configure import ConfigureService
from bob_wemo_service.wemo import WemoAPI
from bob_wemo_service.service_main import MainTask
from bob_wemo_service.tools.ref_num import RefNum
from bob_wemo_service.tools.message_handlers import MessageHandler



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
parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(parent_path, 'config.ini')
print("\n\nUsing Config file:\n" + config_file + "\n\n")
SERVICE_CONFIG = ConfigureService(config_file)
LOG_PATH = SERVICE_CONFIG.get_logger_path()
SERVICE_ADDRESSES = SERVICE_CONFIG.get_servers()
MESSAGE_TYPES = SERVICE_CONFIG.get_message_types()
WEMO_GW = WemoAPI(LOG_PATH)

REF_NUM = RefNum(LOG_PATH)
LOOP = asyncio.get_event_loop()
COMM_HANDLER = MessageHandler(LOG_PATH, LOOP)
MAINTASK = MainTask(
    LOG_PATH,
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
    # Configure logger
    log = setup_function_logger(LOG_PATH, 'Function_Main')

    log.debug('Starting main()')

    # Create incoming message server
    try:
        log.debug('Creating incoming message listening server at [%s:%s]',
                  SERVICE_ADDRESSES['wemo_addr'],
                  SERVICE_ADDRESSES['wemo_port'])
        msg_in_server = asyncio.start_server(
            COMM_HANDLER.handle_msg_in,
            host=SERVICE_ADDRESSES['wemo_addr'],
            port=int(SERVICE_ADDRESSES['wemo_port']))
        log.debug('Wrapping servier in future task and scheduling for '
                  'execution')
        msg_in_task = LOOP.run_until_complete(msg_in_server)
    except Exception:
        log.debug('Failed to create socket listening connection at %s:%s',
                  SERVICE_ADDRESSES['wemo_addr'],
                  SERVICE_ADDRESSES['wemo_port'])
        sys.exit()

    # Create main task for this service
    log.debug('Scheduling main task for execution')
    asyncio.ensure_future(MAINTASK.run())

    # Create outgoing message task
    log.debug('Scheduling outgoing message task for execution')
    asyncio.ensure_future(COMM_HANDLER.handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    log.info('Wemo Gateway Service')
    log.info('Serving on {}'.format(msg_in_task.sockets[0].getsockname()))
    log.info('Press CTRL+C to exit')
    try:
        LOOP.run_forever()
    except asyncio.CancelledError:
        log.info('All tasks have been cancelled')
    except KeyboardInterrupt:
        pass
    finally:
        log.info('Shutting down incoming message server')
        msg_in_server.close()
        log.info('Finding all running tasks to shut down')
        pending = asyncio.Task.all_tasks()
        log.info('[%s] Task still running.  Closing them now', str(len(pending)))
        for i, task in enumerate(pending):
            with suppress(asyncio.CancelledError):
                log.info('Waiting for task [%s] to shut down', i)
                task.cancel()
                LOOP.run_until_complete(task)
        log.info('Shutdown complete.  Terminating execution LOOP')

    # Terminate the execution LOOP
    LOOP.close()


# Call Main *******************************************************************
if __name__ == "__main__":
    main()
