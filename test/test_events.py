#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, MagicMock
from pythoria import events

class TestWeakBoundMEthod(unittest.TestCase):
    def setUp(self):
        self.bm = Mock(name='bound method')
        self.bm.__self__ = Mock(name='self')
        self.bm.__func__ = Mock(name='func')
    
    def test_simple_func(self):
        mock = Mock()
        with self.assertRaises(AssertionError):
            events.WeakBoundMethod(mock)
    
    def test_static_method(self):
        class Mock:
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
        wbm()
        self.bm.__func__.assert_called_with(self.bm.__self__)
        wbm(1, 2, 3)
        self.bm.__func__.assert_called_with(self.bm.__self__, 1, 2, 3)
    
    @unittest.skip
    def test_call_when_dead(self):
        wbm = events.WeakBoundMethod(self.mock.mock_bound)
        del self.mock
        with self.assertRaises(AssertionError):
            wbm()


if __name__ == '__main__':
    unittest.main()
