#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch
from pythoria.messagebox import MessageBox

class TestMessageBox(unittest.TestCase):
    def setUp(self):
        self.msg_box = MessageBox('message1', 'message2')
        
    def test_init(self):
        msg_box = MessageBox()
        self.assertIsInstance(msg_box, MessageBox)
    
    def test_init_with_msgs(self):
        self.assertEqual(self.msg_box, ['message1', 'message2'])
        self.assertNotEqual(self.msg_box, ['message3', 'message4'])
    
    def test_str(self):
        self.assertEqual(str(self.msg_box), 'message1\nmessage2')
    
    def test_add(self):
        import datetime
        with patch.object(self.msg_box, '_now') as mock_now:
            mock_now.return_value = datetime.datetime(2014, 1, 1, 8, 9, 10)
            self.msg_box.add('message3')
            self.assertEqual(self.msg_box, ['message1', 'message2', '[08:09:10] message3'])


if __name__ == '__main__':
    unittest.main()
