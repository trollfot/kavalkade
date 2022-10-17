import asyncio
import typing as t
import logging
from abc import ABC, abstractmethod, abstractproperty


logger = logging.getLogger(__name__)


class Service:
    name: str
    coro: t.Callable[[], t.Coroutine[None, None, None]]
    task: t.Optional[asyncio.Task] = None

    def __init__(self, name, coro):
        self.name = name
        self.coro = coro


class Services:

    _started: bool = False
    _services: t.MutableMapping[str, Service]

    def __init__(
            self,
            loop=None,
            services: t.Optional[t.Mapping[str, Service]] = None):
        if services is None:
            services = {}
        self.loop = loop
        self._services = services

    def bind(self, loop):
        self.loop = loop

    def __len__(self):
        return len(self._services)

    def __getitem__(self, name: str):
        return self._services[name]

    def __contains__(self, name: str):
        return name in self._services

    def remove(self, name: str):
        if self._started:
            self._services[name].stop()
        del self._services[name]

    def add(self, name: str, coro: t.Callable[[], t.Coroutine[None, None, None]]):
        if self._started:
            raise RuntimeError(
                'Services are already started. Cannot add a new one.')
        if name in self._services:
            logger.debug(
                f'Service {name!r} already exists. '
                f'Replacing {self._services[name]} with {coro}'
            )
        self._services[name] = Service(name, coro)
        logger.info(f'Added new service {coro!r} as {name!r}.')

    def register(self, name: str):
        def service_registration(coro: t.Callable[[], t.Coroutine[None, None, None]]):
            self.add(name, coro)
            return coro
        return service_registration

    def __iter__(self):
        return iter(self._services.values())

    def start(self):
        if self._started:
            raise RuntimeError('Services are already started.')
        for name, service in self._services.items():
            service.task = self.loop.create_task(service.coro)
        self._started = True

    def stop(self):
        if not self.started:
            raise RuntimeError('Services are not yet started.')
        for name, service in self._services.items():
            service.task.cancel()
        self._started = False
