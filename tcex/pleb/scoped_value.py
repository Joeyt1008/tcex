# standard library
import os
import threading
import typing
from typing import Any, Callable

import wrapt

T = typing.TypeVar('T')


class scoped_value(typing.Generic[T]):
    def __init__(self):
        self.value = threading.local()

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        if hasattr(self.value, 'data'):
            pid, value = self.value.data
            if pid != os.getpid():
                return self._create_value(wrapped, args, kwargs)

            return value
        else:
            new_value = self._create_value(wrapped, args, kwargs)
            return new_value

    def _create_value(self, wrapped, args, kwargs):
        data = wrapped(*args, **kwargs)
        setattr(self.value, 'data', (os.getpid(), data))
        return data
