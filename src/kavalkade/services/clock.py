from datetime import datetime
from kavalkade.app.services import Service


class Clock(Service):

    def __init__(self, delta: int = 6):
        self.delta = delta

    @property
    def started(self):
        return self._thread is not None

    def clocker(self):
        while True:
            if participants:  # only if there's someone to listen.
                now = datetime.now()
                queue.put(f"It's {now.strftime('%H:%M:%S')}")
                sleep(6)

    def start(self, buses):
        if self.thread is not None:
            raise RuntimeError('Greenthread already running.')
        self._thread = spawn(self.watch)

    def stop(self):
        if self._thread is None:
            raise RuntimeError('Greenthread is not running.')
        self._thread.kill()
        self._thread = None
