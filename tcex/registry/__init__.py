# standard library
from typing import Callable, Type, Union


class ServiceRegistry:
    def __init__(self):
        self.values = {}

    def add(self, type, value):
        self.values[type.__name__] = value

    def add_factory(self, type_or_name: Union[str, Type], factory: Callable, singleton=True):
        key = type_or_name if isinstance(type_or_name, str) else type_or_name.__name__
        self.values[key] = (singleton, factory)

    def get(self, type_or_name):
        key = type_or_name if isinstance(type_or_name, str) else type_or_name.__name__
        if key in self.values:
            value = self.values[key]
            if isinstance(value, tuple):
                singleton, factory = value
                if not singleton:
                    return factory()

                value = factory()
                self.values[key] = value

            return value

        raise RuntimeError(f'No provider for type: {key}')

    @property
    def session_tc(self) -> 'TcSession':
        return self.get('TcSession')

    @property
    def redis_client(self) -> 'RedisClient':
        return self.get('RedisClient')


service_registry = ServiceRegistry()
