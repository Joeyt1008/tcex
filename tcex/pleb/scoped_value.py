"""Declares a scoped_value decorator."""
# standard library
import os
import threading
import typing
from typing import Any, Callable

import wrapt

T = typing.TypeVar('T')


class scoped_value(typing.Generic[T]):
    """Makes a value unique for each thread.

    Essentially, a thread-and-process local value.  When used to decorate a function, will
    treat that function as a factory for the underlying value, and will invoke it to produce a value
    for each thread the value is requested from.

    Note that this also provides a cache: each thread will re-use the value previously created
    for it.
    """
    def __init__(self):
        """Initialize."""
        self.value = threading.local()

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        """Return or create and return a value for the calling thread.

        The wrapped function is treated as a factory, and invoked with the given args and kwargs.
        The wrapped function can be a bound method and will work as expected.
        """
        if hasattr(self.value, 'data'):
            #  A value has been created for this thread already, but we have to make sure we're in
            # the same process (threads are duplicated when a process is forked).
            pid, value = self.value.data
            if pid != os.getpid():
                return self._create_value(wrapped, args, kwargs)

            return value
        else:
            # A value has *not* been created for the calling thread yet, so use the factory to
            # create a new one.
            new_value = self._create_value(wrapped, args, kwargs)
            return new_value

    def _create_value(self, wrapped, args, kwargs):
        """Call the wrapped factory function to get a new value."""
        data = wrapped(*args, **kwargs)
        setattr(self.value, 'data', (os.getpid(), data))
        return data
