import typing as t
from abc import ABC, abstractmethod, abstractproperty


class Bus(ABC):

    @abstractmethod
    def put(self):
        ...

    @abstractmethod
    def get(self):
        ...


class Service(ABC):

    @abstractproperty
    def started(self):
        ...

    @abstractmethod
    def start(self, buses: t.Mapping[str, Bus]):
        ...

    @abstractmethod
    def stop(self):
        ...


class Services(t.Iterable[Service]):
    """Service registry
    """
    buses: t.MutableMapping[str, Bus]
    _services: t.MutableMapping[str, Service]
    _started: bool = False

    def __init__(
            self,
            services: t.Optional[t.Mapping[str, Service]] = None,
            buses: t.Optional[t.Mapping[str, Bus]]] = None):
        if services is None:
            services = {}
        self._services = services
        if buses is None:
            buses = {}
        self._buses = buses

    def __len__(self):
        return len(self._services)

    def __getitem__(self, name: str):
        return self._services[name]

    def __contains__(self, name: str):
        return name in self._services

    @property
    def started(self):
        return self._started

    def get(self, name):
        return self._services.get(name)

    def remove(self, name: str):
        if self._started:
            self._services[name].stop()
        del self._services[name]

    def add(self, name: str, service: Service):
        if self._started:
            raise RuntimeError(
                'Services are already started. Cannot add a new one.')
        if name in self._services:
            logger.debug(
                f'Service {name!r} already exists. '
                f'Replacing {self._services[name]} with {service}'
            )
        self._services[name] = service
        logger.info(f'Added new service {service!r} as {name!r}.')
        return info

    def register(self, name: str):
        def service_registration(service: Service):
            self.add(name, service)
            return service
        return service_registration

    def __iter__(self):
        return iter(self._services.values())

    def start(self):
        if self.started:
            raise RuntimeError('Services are already started.')
        for name, service in self._services.items():
            service.start(self.buses)
        self._started = True

    def stop(self):
        if not self.started:
            raise RuntimeError('Services are not yet started.')
        for name, service in self._services.items():
            service.stop()
        self._started = False
