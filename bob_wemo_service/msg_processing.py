#!/usr/bin/python3
""" msg_processing.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bob_wemo_service.messages.heartbeat import HeartbeatMessage
from bob_wemo_service.messages.heartbeat_ack import HeartbeatMessageACK
from bob_wemo_service.messages.get_device_state import GetDeviceStateMessage
from bob_wemo_service.messages.get_device_state_ack import GetDeviceStateMessageACK
from bob_wemo_service.messages.set_device_state import SetDeviceStateMessage
from bob_wemo_service.messages.set_device_state_ack import SetDeviceStateMessageACK


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


def create_heartbeat_msg(logger, ref_num, destinations, source_addr, source_port, message_types):
    """ function to create one or more heartbeat messages """
    # Configure loggers
    logger = logger or logging.getLogger(__name__)

    # Initialize result list
    out_msg_list = []

    # Generate a heartbeat message for each destination given
    for entry in destinations:
        out_msg = HeartbeatMessage(
            logger=logger,
            ref=ref_num.new(),
            dest_addr=entry[0],
            dest_port=entry[1],
            source_addr=source_addr,
            source_port=source_port,
            msg_type=message_types['heartbeat']
        )
        # Load message into output list
        logger.debug('Loading completed msg: %s', out_msg.complete)
        out_msg_list.append(copy.copy(out_msg.complete))

    # Return response message
    return out_msg_list


def process_heartbeat_msg(logger, ref_num, msg, message_types):
    """ function to ack wake-up requests to wemo service """
    # Configure loggers
    logger = logger or logging.getLogger(__name__)

    # Initialize result list
    out_msg_list = []

    # Map message into wemo wake-up message class
    message = HeartbeatMessage(logger=logger)
    message.complete = msg

    # Send response indicating query was executed
    logger.debug('Building response message header')
    out_msg = HeartbeatMessageACK(
        logger=logger,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['heartbeat_ack'])

    # Load message into output list
    logger.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(copy.copy(out_msg.complete))

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo get status *****************************
@asyncio.coroutine
def get_wemo_state(logger, ref_num, wemo_gw, msg, message_types):
    """ Function to properly process wemo device status requests """
    # Configure loggers
    logger = logger or logging.getLogger(__name__)

    # Initialize result list
    out_msg_list = []

    # Map message into GDS message class
    message = GetDeviceStateMessage(logger=logger)
    message.complete = msg    

    # Execute Status Update
    logger.debug('Requesting status for [%s] at [%s] with original status '
                 '[%s] and update time [%s]',
                 message.dev_name,
                 message.dev_addr,
                 message.dev_status,
                 message.dev_last_seen)
    dev_status_new, dev_last_seen_new = wemo_gw.read_status(
        message.dev_name,
        message.dev_addr,
        message.dev_status,
        message.dev_last_seen)

    # Send response indicating query was executed
    logger.debug('Building response message header')
    out_msg = GetDeviceStateMessageACK(
        logger=logger,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['get_device_state_ack'],
        dev_name=message.dev_name,
        dev_status=str(dev_status_new),
        dev_last_seen=str(dev_last_seen_new)[:19])

    # Load message into output list
    logger.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(copy.copy(out_msg.complete))

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def set_wemo_state(logger, ref_num, wemo_gw, msg, message_types):
    """ Function to set state of wemo device to "on" """
    # Configure loggers
    logger = logger or logging.getLogger(__name__)

    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = SetDeviceStateMessage(logger=logger)
    message.complete = msg

    # Execute wemo on commands
    if message.dev_cmd == '1' or message.dev_cmd == 'on':
        logger.debug('Commanding wemo device [%s] to "on"', message.dev_name)
        dev_status_new, dev_last_seen_new = wemo_gw.turn_on(
            message.dev_name,
            message.dev_addr,
            message.dev_last_seen)

    # Execute wemo off commands
    elif message.dev_cmd == '0' or message.dev_cmd == 'off':
        logger.debug('Commanding wemo device [%s] to "off"', message.dev_name)
        dev_status_new, dev_last_seen_new = wemo_gw.turn_off(
            message.dev_name,
            message.dev_addr,
            message.dev_last_seen)

    # If command not valid, leave device un-changed
    else:
        logger.warning('Invalid command [%s] for device [%s]',
                       message.dev_cmd,
                       message.dev_name)
        dev_status_new = copy.copy(message.dev_status)
        dev_last_seen_new = copy.copy(message.dev_last_seen)

    # Send response indicating command was executed
    logger.debug('Building response message')
    out_msg = SetDeviceStateMessageACK(
        logger=logger,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['set_device_state_ack'],
        dev_name=message.dev_name,
        dev_status=dev_status_new,
        dev_last_seen=dev_last_seen_new)

    # Load message into output list
    logger.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(copy.copy(out_msg.complete))

    # Return response message
    return out_msg_list
