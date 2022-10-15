from datetime import datetime
from eventlet import sleep
from . import GreenService


class Clock(GreenService):

    def __init__(self, websockets, delta: int = 6):
        self.delta = delta
        self.websockets = websockets

    def __repr__(self):
        return f"<Clock every {self.delta}sec>"

    def runner(self):
        while True:
            if self.websockets:  # only if there's someone to listen.
                now = datetime.now()
                self.websockets.broadcast(
                    f"It's {now.strftime('%H:%M:%S')}")
            sleep(self.delta)
