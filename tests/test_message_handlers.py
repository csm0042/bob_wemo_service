#!/usr/bin/python3
""" test_message_handlers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import logging
import unittest
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bob_wemo_service.message_handlers import MessageHandler


# Define test class ***********************************************************
class TestMessageHandler(unittest.TestCase):
    """ unittests for Message handler Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.datetime = datetime.datetime
        self.datetime_str = str(self.datetime)
        self.loop = asyncio.get_event_loop()
        self.mh = MessageHandler(self.loop, logger=self.log)
        super(TestMessageHandler, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestMessageHandler, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        self.assertEqual(self.mh.logger, self.log)
        self.assertEqual(self.mh.loop, self.loop)


    def test_handle_msg_in(self):
        """ test setting and getting message reference number field """
        self.msg_in_server = asyncio.start_server(
            self.mh.handle_msg_in,
            host='127.0.0.1',
            port=27099)
        self.msg_in_task = self.loop.run_until_complete(self.msg_in_server)
        #self.loop.run_forever()
        # Put code here to open socket and send something to msg_in handler
        self.assertEqual(self.mh.msg_in_queue.qsize(), 0)
        self.msg_in_server.close()


    def test_handle_msg_out(self):
        """ test setting and getting message reference number field """
        asyncio.ensure_future(self.mh.handle_msg_out())
        #self.loop.run_forever()
        # Put code here to open socket and send something to msg_in handler
        self.assertEqual(self.mh.msg_out_queue.qsize(), 0)
        asyncio.Task.all_tasks()


if __name__ == "__main__":
    unittest.main()
