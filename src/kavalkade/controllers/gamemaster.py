import os
import struct
import inotify.adapters
from datetime import datetime
from threading import Thread, currentThread
from eventlet import websocket, green, queue, sleep, GreenPool, spawn
from kavalkade.controllers import router
from kavalkade.utils import INotifyWatcher
from knappe.decorators import html


participants = set()


@router.register('/talk')
@html('websocket')
def gamemaster_chat(ws):
    return {}


def check_folder(*paths):
    events = INotifyWatcher(*paths).watch()
    while event := next(events):
        if participants:
            parts = [event.path, event.get_mask_description()]
            if event.name:
                parts.append(event.name)
            msg = ' '.join(parts)
            for participant in participants:
                participant.send(f"File event: {msg}")


def clock_every_6_sec(queue):
    while True:
        if participants:  # only if there's someone to listen.
            now = datetime.now()
            queue.put(f"It's {now.strftime('%H:%M:%S')}")
            sleep(6)


incoming_events = queue.Queue()
clocker = None
watcher = None


def read_ws(ws):
    while True:
        m = ws.wait()
        if m is None:
            break
        for p in participants:
            p.send(m)


def read_events(queue):
    while True:
        m = incoming_events.get()
        for p in participants:
            p.send(m)


@websocket.WebSocketWSGI
def chat(ws):
    global clocker, watcher

    if clocker is None:
        clocker = spawn(clock_every_6_sec, incoming_events)
    if watcher is None:
        watcher = spawn(check_folder, '/tmp')

    participants.add(ws)
    try:
        pool = GreenPool()
        ws_reader = pool.spawn(read_ws, ws)
        iq_reader = pool.spawn(read_events, incoming_events)
        ws_reader.wait()
    finally:
        ws_reader.kill()
        iq_reader.kill()
        participants.remove(ws)
