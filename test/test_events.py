#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch
from pythoria import events


class TestConnection(unittest.TestCase):
    def test_cleanup_on_delete(self):
        ev_disp = Mock(name="Event Dispatcher")
        self.conn = events.Connection(ev_disp, Mock(), Mock())
        del self.conn
        self.assertTrue(ev_disp.remove.called)

class Observer:
    """Dummy class for testing the EventDispatcher"""
    called = False
    
    def on_post(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs

class TestEventDispatcher(unittest.TestCase):
    def setUp(self):
        self.observer = Observer()
        self.ed = events.EventDispatcher()
        self.connection = self.ed.bind('test_event', self.observer.on_post)
    
    def test_bind(self):
        self.assertIs(self.connection.event_type, 'test_event')
        self.assertEqual(self.connection.listener(), self.observer.on_post)

    def test_post(self):
        self.ed.post('test_event', 2, b=3)
        self.assertTrue(self.observer.called)
        self.assertEqual(self.observer.args, (2,))
        self.assertEqual(self.observer.kwargs, {'b': 3})

    def test_post_inexistant_event(self):
        self.ed.post('inexistant event', 2, b=3)
        self.assertFalse(self.observer.called)
    
    def test_remove(self):
        self.ed.remove(self.connection)
        self.ed.post('test_event', 2, b=3)
        self.assertFalse(self.observer.called)
        

if __name__ == '__main__':
    unittest.main()
