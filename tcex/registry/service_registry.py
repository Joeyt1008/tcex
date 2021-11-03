"""A service registry."""
# standard library
from typing import Callable, Type, Union, Tuple, Any
from collections.abc import Container


class ServiceRegistry(Container):
    """Dynamic service registry that supports raw values, factories, and factory providers.

    Terms:
        Service - An object that is registered with this registry and can be retrieved from it by
            type or name.
        Factory - A callable that can return an instance that fulfills a type or name.
        Provider - An object with one or more members that are factories (as denoted by the
            @factory decorator)
    """
    def __init__(self):
        """."""
        self._values = {}

    def add_service(self, type_or_name: Union[str, Type], value: Any):
        """Add an instance of a type to this registry.

        A service is a single instance of the given type.

        Args:
            type_or_name: the concrete type of the provided service, or a name (MyClass or
            'MyClass')
            value: The service.
        """
        self._add(type_or_name, value)

    def add_factory(self, type_or_name: Union[str, Type], factory: Callable, singleton=False):
        """Add a factory for a service.

        A factory is any callable that can be invoked to provide the given type of service.

        Args:
            type_or_name: the concrete type of the provided service, or a name (MyClass or
            'MyClass')
            factory: the callable that can create the above type.
            singleton: if True, the factory will be invoked exactly once.  If False, the factory
            will be invoked every time the service is requested.
        """
        self._add(type_or_name, (singleton, factory))

    def add_service_provider(self, provider):
        """Add a provider, which provides one or more service factories.

        A provider is a class with one or more members decorated with ServiceRegistry@factory.
        When you add a provider with this method, each of its decorated members will be added to
        this registry as a factory.
        """
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
        """Enable property-access style access to registered services, i.e., registry.MyClass."""
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
        """Enable the syntax MyClass in registry."""
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
        """Decorator for a function that can be treated as a factory that provides a service.

        Args:
            type_or_name: the concrete type of the provided service, or a name (MyClass or
            'MyClass')
            singleton: if True, the factory will be invoked exactly once.  If False, the factory
            will be invoked every time the service is requested.
        """
        def _decorator(original):
            setattr(original, 'factory_provider', (type_or_name, singleton))
            return original

        return _decorator

    #
    # The below are convenience-wrappers that make it easier to retrieve well-known services.
    #

    @property
    def session_tc(self) -> 'TcSession':
        """Convenience wrapper to return a TcSession."""
        return self.TcSession

    @property
    def redis_client(self) -> 'Redis':
        """Convenience wrapper to return a Redis client object (redis.Redis)."""
        return self.Redis

    @property
    def key_value_store(self) -> Union['KeyValueRedis', 'KeyValueApi']:
        """Convenience wrapper to return a KeyValue object, either an API version or a Redis one."""
        return self.KeyValueStore

    @property
    def playbook(self) -> 'Playbook':
        """Convenience wrapper to return a Playbook object."""
        return self.Playbook


registry = ServiceRegistry()

