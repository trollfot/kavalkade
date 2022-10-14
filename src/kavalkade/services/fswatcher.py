import os
import sys
import struct
import inotifyx
from eventlet.green import select
from kavalkade.app.services import Service
from eventlet import spawn


_EVENT_FMT = 'iIII'
_EVENT_SIZE = struct.calcsize(_EVENT_FMT)
_BUF_LEN = 1024 * (_EVENT_SIZE + 16)
ENCODING = sys.getfilesystemencoding()


class INotifyWatcher:

    def __init__(self, *paths):
        self.running = True
        self.wd_to_path = {}
        self.fd = inotifyx.init()
        for path in paths:
            wd = inotifyx.add_watch(self.fd, path)
            self.wd_to_path[wd] = path

    def watch(self, timeout=None):
        try:
            while self.running:
                rlist, _, _ = select.select([self.fd], [], [], timeout)
                buf = os.read(self.fd, _BUF_LEN)
                i = 0
                while i < len(buf):
                    (wd, mask, cookie, len_) = struct.unpack_from(
                        _EVENT_FMT, buf, i
                    )
                    name = None
                    if len_ > 0:
                        start = i + _EVENT_SIZE
                        end = start + len_
                        # remove \0 terminator and padding
                        name = buf[start:end].rstrip(b'\0').decode(ENCODING)

                    event = inotifyx.InotifyEvent(wd, mask, cookie, name)
                    event.path = self.wd_to_path[wd]
                    yield event
                    i += _EVENT_SIZE + len_
        finally:
            yield None
            self.fd.close()


class FileSystemWatcher(Service):

    def __init__(self, paths):
        self.paths = paths
        self._thread = None

    @property
    def started(self):
        return self._thread is not None

    def watch(self):
        events = INotifyWatcher(*self.paths).watch()
        while event := next(events):
            if participants:
                parts = [event.path, event.get_mask_description()]
                if event.name:
                    parts.append(event.name)
                msg = ' '.join(parts)
                for participant in participants:
                    participant.send(f"File event: {msg}")

    def start(self, buses):
        if self.thread is not None:
            raise RuntimeError('Greenthread already running.')
        self._thread = spawn(self.watch)

    def stop(self):
        if self._thread is None:
            raise RuntimeError('Greenthread is not running.')
        self._thread.kill()
        self._thread = None
