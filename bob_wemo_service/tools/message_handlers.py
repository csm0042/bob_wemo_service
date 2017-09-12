#!/usr/bin/python3
""" message_handlers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import os
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


# Message Handler Class Def ***************************************************
class MessageHandler(object):
    def __init__(self, log, loop):
        self.log = log
        self.loop = loop
        self.msg_in_queue = asyncio.Queue()
        self.msg_out_queue = asyncio.Queue()
        self.data_in = None
        self.message = None
        self.addr = None
        self.msg_seg = []
        self.ack_to_send = str()
        self.reader = None
        self.writer = None
        self.msg_to_send = None
        self.msg_seg_out = []
        self.reader_out = None
        self.writer_out = None
        self.ack = str()
        self.data_ack = str()

    # Incoming message handler ************************************************
    @asyncio.coroutine
    def handle_msg_in(self, reader, writer):
        """ Callback used to send ACK messages back to acknowledge messages
        received """
        self.reader = reader
        self.writer = writer
        # Set up socket pair
        self.log.debug('Yielding to reader.read()')
        self.data_in = yield from self.reader.read(200)
        self.log.debug('Decoding read data')
        self.message = self.data_in.decode()
        self.log.debug('Extracting address from socket connection')
        self.addr = self.writer.get_extra_info('peername')
        self.log.debug('Received %r from %r', self.message, self.addr)

        # Coping incoming message to message buffer
        self.log.info('Received message: %s', self.message)
        self.msg_in_queue.put_nowait(self.message)
        self.log.debug('Resulting buffer length: %s',
                       str(self.msg_in_queue.qsize()))

        # Acknowledge receipt of message
        self.log.debug("ACK'ing message: %r", self.message)
        self.log.debug('Splitting message into constituent parts')
        self.msg_seg = self.message.split(',')
        self.log.debug('Extracted msg sequence number: [%s]', self.msg_seg[0])
        self.ack_to_send = self.msg_seg[0].encode()
        self.log.info('Sending ACK: %s', self.ack_to_send)
        self.writer.write(self.ack_to_send)
        yield from writer.drain()
        self.log.debug('Closing the socket after sending ACK')
        self.writer.close()


    # Outgoing message handler ************************************************
    @asyncio.coroutine
    def handle_msg_out(self):
        """ task to handle outgoing messages """
        while True:
            if self.msg_out_queue.qsize() > 0:
                self.log.debug('Pulling next outgoing message from queue')
                self.msg_to_send = self.msg_out_queue.get_nowait()
                self.log.debug('Extracting msg destination address and port')
                self.msg_seg_out = self.msg_to_send.split(',')
                self.log.debug('Opening outgoing connection to %s:%s',
                               self.msg_seg_out[1], self.msg_seg_out[2])
                try:
                    self.reader_out, self.writer_out = yield from asyncio.open_connection(
                        self.msg_seg_out[1], int(self.msg_seg_out[2]), loop=self.loop)
                    self.log.info('Sending message: %s', self.msg_to_send)
                    self.writer_out.write(self.msg_to_send.encode())

                    self.log.info('Waiting for ack')
                    self.data_ack = yield from self.reader_out.read(200)
                    self.ack = self.data_ack.decode()
                    self.log.info('Received ACK: %r', self.ack)
                    if self.ack.split(',')[0] == self.msg_seg_out[0]:
                        self.log.debug('Successful ACK received')
                    else:
                        self.log.debug('Ack received does not match sent '
                                       'message')
                    self.log.debug('Closing socket')
                    self.writer_out.close()
                except Exception:
                    self.log.warning('Could not open socket connection to '
                                     'target')
            # Yield to other tasks for a while
            yield from asyncio.sleep(0.25)

