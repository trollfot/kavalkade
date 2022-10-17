from abc import abstractmethod
from kavalkade.app.services import Service
from eventlet import spawn


class GreenService(Service):

    _thread = None

    @property
    def started(self):
        return self._thread is not None

    def start(self):
        if self._thread is not None:
            raise RuntimeError('Greenthread already running.')
        self._thread = spawn(self.runner)

    def stop(self):
        if self._thread is None:
            raise RuntimeError('Greenthread is not running.')
        self._thread.kill()
        self._thread = None

    @abstractmethod
    def runner(self):
        ...
