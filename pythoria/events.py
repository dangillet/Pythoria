#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# From http://stackoverflow.com/a/7294148/893822

import weakref

class WeakBoundMethod:
    """
    Wrapper around a method bound to a class instance. As opposed to bare
    bound methods, it holds only a weak reference to the `self` object,
    allowing it to be deleted.

    This can be useful when implementing certain kinds of systems that
    manage callback functions, such as an event manager.

    """
    def __init__(self, meth):
        """
        Initializes the class instance. It should be ensured that methods
        passed through the `meth` parameter are always bound methods. Static
        methods and free functions will produce an `AssertionError`.

        """
        assert (hasattr(meth, '__func__') and hasattr(meth, '__self__')),\
               'Object is not a bound method.'

        self._self = weakref.ref(meth.__self__)
        self._func = meth.__func__

    def __call__(self, *args, **kw):
        """
        Calls the bound method and returns whatever object the method returns.
        Any arguments passed to this will also be forwarded to the method.

        In case an exception is raised by the bound method, it will be
        caught and thrown again to the caller of this `WeakBoundMethod` object.

        Calling this on objects that have been collected will result in
        an `AssertionError` being raised.

        """        
        assert self.alive(), 'Bound method called on deleted object.'

        try:
            return self._func(self._self(), *args, **kw)
        except Exception as e:
            raise e

    def alive(self):
        """
        Checks whether the `self` object the method is bound to has
        been collected.

        """
        return self._self() is not None


class Connection:
    """
    A Connection object knows the listener weakboundmethod for a given
    event class (event type) in an event dispatcher.
    When the Connection gets deleted, it asks the event dispatcher to remove
    itself from its dict of listeners.
    
    A Connection is normally created by the event dispatcher when a listener
    adds itself for some event type notifications.
    """
    def __init__(self, event_dispatcher, eventcls, listener):
        """
        event_dispatcher is the object which created the Connection.
        eventcls is the type of event this connection is linked to.
        listener is the weak bound method called when the event eventcls is
        posted.
        """
        self.ed = event_dispatcher
        self.eventcls = eventcls
        self.listener = listener
    
    def __del__(self):
        """
        When the connection gets deleted, the event dispatcher removes the
        weak bound method from its dict of listeners for the given event class.
        """
        self.ed.remove(self)
        
        
class EventDispatcher:
    """
    Class that implements events dispatching. Listeners register their
    bound method for a given event type (class).
    """
    def __init__(self):
        # Dict that maps event types to lists of listeners
        self._listeners = dict()

    def add(self, eventcls, listener):
        """
        eventcls is the class of the event type the listener want to get notified
        about.
        listener is a bound method of the listener. It will get called with
        the event in argument when the post method is called.
        Returns a connection object which when deleted will remove the weak
        bound method from the listeners dict.
        """
        listener = WeakBoundMethod(listener)
        self._listeners.setdefault(eventcls, list()).append(listener)
        return Connection(self, eventcls, listener)

    def post(self, event):
        """
        Post an event to the interested weak bound methods registered with the
        add method.
        """
        try:
            for listener in self._listeners[event.__class__]:
                listener(event)
        except KeyError:
            pass # No listener interested in this event
    
    def remove(self, connection):
        """
        Removes a weak bound method for a given event class. The connection
        object contains this information.
        """
        self._listeners[connection.eventcls].remove(connection.listener)
        

if __name__ == '__main__':
    """
    Creates a Dummy Event for a dummy Controller. Check if posting the 
    DummyEvent works and if the listener is removed when the controller
    gets deleted (and so the connection object it contains).
    """

    class DummyEvent:
        pass
    
    class Controller:
        def __init__(self, event_dispatcher):
            self.ed = event_dispatcher
            self._connection = self.ed.add(DummyEvent, self.on_event)
        
        def on_event(self, e):
            print("In the on_event method")
            print("event is {}".format(e))
            
    ed = EventDispatcher()
    cont = Controller(ed)
    ed.post(DummyEvent())
    

    del cont
    print(ed._listeners)

    


