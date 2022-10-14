import os
import sys
import struct
import inotifyx
import contextlib
import functools
from eventlet import green


_EVENT_FMT = 'iIII'
_EVENT_SIZE = struct.calcsize(_EVENT_FMT)
_BUF_LEN = 1024 * (_EVENT_SIZE + 16)
ENCODING = sys.getfilesystemencoding()


def get_inotify_events(fd, timeout=None):
    """get_events(fd[, timeout])
    Return a list of InotifyEvent instances representing events read from
    inotify.  If timeout is None, this will block forever until at least one
    event can be read.  Otherwise, timeout should be an integer or float
    specifying a timeout in seconds.  If get_events times out waiting for
    events, an empty list will be returned.  If timeout is zero, get_events
    will not block.
    This version of get_events() will only block the current eventlet.
    """
    (rlist, _, _) = green.select.select([fd], [], [], timeout)
    if not rlist:
        return []
    events = []

    while True:
        buf = os.read(fd, _BUF_LEN)
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

            events.append(inotifyx.InotifyEvent(wd, mask, cookie, name))
            i += _EVENT_SIZE + len_

        (rlist, _, _) = green.select.select([fd], [], [], 0)
        if not rlist:
            break

    return events


@contextlib.contextmanager
def inotify_watcher(*paths):
    fd = inotifyx.init()
    wd_to_path = {}
    try:
        for path in paths:
            wd = inotifyx.add_watch(fd, path)
            wd_to_path[wd] = path
        yield functools.partial(get_inotify_events, fd)
    finally:
        os.close(fd)
