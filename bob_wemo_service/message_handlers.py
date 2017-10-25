#!/usr/bin/python3
""" message_handlers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import logging


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The B.O.B. Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Message Handler Class Def ***************************************************
class MessageHandler(object):
    def __init__(self, loop, logger=None):
        # Configure loggers
        self.logger = logger or logging.getLogger(__name__)

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
        self.sleep_time = 0.2

    # Incoming message handler ************************************************
    @asyncio.coroutine
    def handle_msg_in(self, reader, writer):
        """ Callback used to send ACK messages back to acknowledge messages
        received """
        self.reader = reader
        self.writer = writer
        # Set up socket pair
        self.logger.debug('Yielding to reader.read()')
        self.data_in = yield from self.reader.read(200)
        self.logger.debug('Decoding read data')
        self.message = self.data_in.decode()
        self.logger.debug('Extracting address from socket connection')
        self.addr = self.writer.get_extra_info('peername')
        self.logger.debug(
            'Received %r from %r',
            self.message,
            self.addr
        )

        # Coping incoming message to message buffer
        self.logger.debug('Received message: %s', self.message)
        self.msg_in_queue.put_nowait(self.message)
        self.logger.debug('Resulting buffer length: %s',
                          str(self.msg_in_queue.qsize()))

        # Acknowledge receipt of message
        self.logger.debug("ACK'ing message: %r", self.message)
        self.logger.debug('Splitting message into constituent parts')
        self.msg_seg = self.message.split(',')
        self.logger.debug(
            'Extracted msg sequence number: [%s]',
            self.msg_seg[0]
        )
        self.ack_to_send = self.msg_seg[0].encode()
        self.logger.debug('Sending ACK: %s', self.ack_to_send)
        self.writer.write(self.ack_to_send)
        yield from writer.drain()
        self.logger.debug('Closing the socket after sending ACK')
        self.writer.close()


    # Outgoing message handler ************************************************
    @asyncio.coroutine
    def handle_msg_out(self):
        """ task to handle outgoing messages """
        while True:
            self.sleep_time = 0.2
            if self.msg_out_queue.qsize() > 0:
                self.sleep_time = 0.05
                self.logger.debug(
                    'Pulling next outgoing message from queue'
                )
                self.msg_to_send = self.msg_out_queue.get_nowait()
                self.logger.debug(
                    'Preparing to send message: %s',
                    self.msg_to_send
                )
                self.logger.debug(
                    'Extracting msg destination address and port'
                )
                self.msg_seg_out = self.msg_to_send.split(',')
                self.logger.debug(
                    'Opening outgoing connection to %s:%s',
                    self.msg_seg_out[1],
                    self.msg_seg_out[2]
                )
                try:
                    self.reader_out, self.writer_out = yield from asyncio.open_connection(
                        self.msg_seg_out[1],
                        int(self.msg_seg_out[2]),
                        loop=self.loop
                    )
                    self.logger.debug('Sending message: %s', self.msg_to_send)
                    self.writer_out.write(self.msg_to_send.encode())

                    self.logger.debug('Waiting for ack')
                    self.data_ack = yield from self.reader_out.read(200)
                    self.ack = self.data_ack.decode()
                    self.logger.debug('Received ACK: %r', self.ack)
                    self.logger.debug('Closing socket')
                    self.writer_out.close()
                except Exception:
                    self.logger.warning(
                        'Could not open socket connection to target'
                    )
            # Yield to other tasks for a while
            yield from asyncio.sleep(self.sleep_time)
