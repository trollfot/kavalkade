import asyncio
import typing as t
import logging
from contextlib import suppress
from abc import ABC, abstractmethod, abstractproperty


logger = logging.getLogger(__name__)


class Service:
    __slots__ = ('name', 'coro', 'task')

    name: str
    coro: t.Callable[[], t.Coroutine[None, None, None]]
    task: t.Optional[asyncio.Task]

    def __init__(self, name, coro):
        self.name = name
        self.coro = coro
        self.task = None

    @property
    def started(self):
        return self.task is not None

    @property
    def status(self):
        try:
            result = self.task.result()
        except asyncio.CancelledError:
            # the task has been cancelled
            return 'Cancelled'
        except Exception as exc:
            if isinstance(exc, asyncio.exceptions.InvalidStateError):
                return 'Running'
            return 'RuntimeError'
        return 'Unknown state'



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

    def _service_callback(self, task: asyncio.Task) -> None:
        try:
            task.result()
        except asyncio.CancelledError:
            pass  # Task cancellation should not be logged as an error.
        except Exception:  # pylint: disable=broad-except
            logger.exception('Exception raised by task = %r', task)

    def start(self):
        if self._started:
            raise RuntimeError('Services are already started.')
        for name, service in self._services.items():
            service.task = self.loop.create_task(service.coro)
            service.task.add_done_callback(self._service_callback)
        self._started = True

    async def stop(self):
        if not self._started:
            raise RuntimeError('Services are not yet started.')
        for name, service in self._services.items():
            logger.info(f'Cancelling service {name!r}.')
            service.task.cancel()
            with suppress(asyncio.CancelledError):
                await service.task
        self._started = False
