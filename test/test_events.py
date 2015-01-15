#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch
from pythoria import events


class TestWeakBoundMethod(unittest.TestCase):
    def setUp(self):
        class MockClass:
            def mock_bound(self, *args, **kwargs):
                return args, kwargs
                
        self.bm = MockClass().mock_bound
    
    def test_simple_func(self):
        mock = Mock()
        with self.assertRaises(AssertionError):
            events.WeakBoundMethod(mock)
    
    def test_static_method(self):
        class MockClass:
            @staticmethod
            def mock():
                pass
        with self.assertRaises(AssertionError):
            events.WeakBoundMethod(Mock().mock)
    
    def test_bound_method(self):
        self.assertIsInstance(events.WeakBoundMethod(self.bm),
                                events.WeakBoundMethod)
    
    def test_call(self):
        wbm = events.WeakBoundMethod(self.bm)
        self.assertEqual(wbm(), ((), {}))
        self.assertEqual(wbm(1, 2, 3), ((1, 2, 3), {}))
        self.assertEqual(wbm(a=1, b=2, c=3), ((), {'a':1, 'b':2, 'c':3}))
        
    def test_call_when_dead(self):
        wbm = events.WeakBoundMethod(self.bm)
        del self.bm
        with self.assertRaises(AssertionError):
            wbm()


class TestConnection(unittest.TestCase):
    def test_cleanup_on_delete(self):
        ev_disp = Mock(name="Event Dispatcher")
        self.conn = events.Connection(ev_disp, Mock(), Mock())
        del self.conn
        self.assertTrue(ev_disp.remove.called)


class TestEventDispatcher(unittest.TestCase):
    def setUp(self):
        patcher_wbm = patch('pythoria.events.WeakBoundMethod', autospec=True)
        self.WeakBoundMethod = patcher_wbm.start()
        self.addCleanup(patcher_wbm.stop)
        
        self.listener = Mock(name="listener")
        self.listener_wbm = self.WeakBoundMethod.return_value
        self.ed = events.EventDispatcher()
        self.connection = self.ed.bind('test_event', self.listener)
    
    def test_bind(self):
        self.assertIs(self.connection.event_type, 'test_event')
        self.assertIs(self.connection.listener, self.listener_wbm)

    def test_post(self):
        self.ed.post('test_event', 2, b=3)
        self.listener_wbm.assert_called_with(2, b=3)
        
        self.listener_wbm.reset_mock()
        self.ed.post('inexistant event', 2, b=3)
        self.assertFalse(self.listener_wbm.called)
    
    def test_remove(self):
        self.ed.remove(self.connection)
        self.ed.post('test_event', 2, b=3)
        self.assertFalse(self.listener_wbm.called)
        

if __name__ == '__main__':
    unittest.main()
