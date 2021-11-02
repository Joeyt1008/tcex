# standard library
import os
import threading
from typing import Any, Callable


class ScopedValue:
    def __init__(self, factory: Callable[[Any], Any]):
        self.value = threading.local()
        self.factory = factory

    def __call__(self, *args, **kwargs):
        try:
            pid, value = self.value.data
            if pid != os.getpid():
                return self._create_value(*args, **kwargs)

            return value
        except AttributeError:
            new_value = self._create_value(*args, **kwargs)
            return new_value

    def _create_value(self, *args, **kwargs):
        data = self.factory(*args, **kwargs)
        setattr(self.value, 'data', (os.getpid(), data))
        return data
