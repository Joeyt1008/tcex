# standard library
from typing import Callable, Type, Union, Tuple
from collections.abc import Container


class ServiceRegistry(Container):
    def __init__(self):
        self._values = {}

    def add_service(self, type_or_name: Union[str, Type], value):
        self._add(type_or_name, value)

    def add_factory(self, type_or_name: Union[str, Type], factory: Callable, singleton=False):
        self._add(type_or_name, (singleton, factory))

    def add_service_provider(self, provider):
        for entry in dir(provider):
            try:
                provider_function = type(provider).__dict__[entry]
                factory_provider = getattr(provider_function, 'factory_provider', None)
                if factory_provider:
                    provider_member = getattr(provider, entry)
                    provided_type, singleton = factory_provider
                    if not callable(provider_member):
                        raise RuntimeError(
                            f'Provider {provider.__class__.__name__} registered '
                            f'{provider_member.__name__}, but it is not callable.')
                    self.add_factory(provided_type, provider_member, singleton)
                value_provider = getattr(provider_function, 'value_provider', None)
                if value_provider:
                    provider_member = getattr(provider, entry)
                    provided_type = value_provider
                    if callable(provider_member):
                        self.add_factory(provided_type, provider_member, singleton=True)
                    else:
                        self.add_service(provided_type, provider_member)
            except KeyError:
                pass

    def _add(self, type_or_name: Union[str, Type], value: Union[Type, Tuple[bool, Callable]]):
        key = type_or_name if isinstance(type_or_name, str) else type_or_name.__name__
        if key in self._values:
            raise RuntimeError(f'A service has already been provided for {key}.')

        self._values[key] = value

    def __getattr__(self, type_or_name):
        key = type_or_name if isinstance(type_or_name, str) else type_or_name.__name__
        if key in self._values:
            value = self._values[key]
            if isinstance(value, tuple):
                singleton, factory = value
                if not singleton:
                    return factory()

                value = factory()
                self._values[key] = value

            return value

        raise RuntimeError(f'No provider for type: {key}')

    def __contains__(self, item) -> bool:
        try:
            self.get(item)
            return True
        except RuntimeError:
            return False

    def _reset(self):
        """Only used during testing to reset registry."""
        self._values = {}

    @staticmethod
    def factory(type_or_name: Union[str, Type], singleton: bool = False):
        def _decorator(original):
            setattr(original, 'factory_provider', (type_or_name, singleton))
            return original

        return _decorator

    @staticmethod
    def service(type_or_name: Union[str, Type]):
        def _decorator(original):
            setattr(original, 'value_provider', type_or_name)
            return original
        return _decorator

    @property
    def session_tc(self) -> 'TcSession':
        return self.TcSession

    @property
    def redis_client(self) -> 'Redis':
        return self.Redis

    @property
    def key_value_store(self) -> Union['KeyValueRedis', 'KeyValueApi']:
        return self.KeyValueStore

    @property
    def playbook(self) -> 'Playbook':
        return self.Playbook


registry = ServiceRegistry()

