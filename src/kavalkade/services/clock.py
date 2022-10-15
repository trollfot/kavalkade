from datetime import datetime
from kavalkade.app.services import Service
from eventlet import spawn, sleep


class Clock(Service):

    def __init__(self, websockets, delta: int = 6):
        self.delta = delta
        self.websockets = websockets
        self._thread = None

    @property
    def started(self):
        return self._thread is not None

    def clocker(self):
        while True:
            if self.websockets:  # only if there's someone to listen.
                now = datetime.now()
                self.websockets.broadcast(f"It's {now.strftime('%H:%M:%S')}")
            sleep(6)

    def start(self):
        if self._thread is not None:
            raise RuntimeError('Greenthread already running.')
        self._thread = spawn(self.clocker)

    def stop(self):
        if self._thread is None:
            raise RuntimeError('Greenthread is not running.')
        self._thread.kill()
        self._thread = None
