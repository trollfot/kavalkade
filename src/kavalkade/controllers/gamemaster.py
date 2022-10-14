import select
from time import sleep
from datetime import datetime
from threading import Thread, currentThread
from multiprocessing import Queue
from eventlet import websocket
from kavalkade.controllers import router
from knappe.decorators import html


participants = set()



@router.register('/talk')
@html('websocket')
def gamemaster_chat(ws):
    return {}


def clock_eveyt_6_sec(queue):
    t = currentThread()
    while getattr(t, "do_run", True):
        now = datetime.now()
        queue.put(f"It's {now.strftime('%H:%M:%S')}")
        sleep(6)


@websocket.WebSocketWSGI
def chat(ws):
    incoming_events = Queue()
    worker = Thread(target=clock_eveyt_6_sec, args=(incoming_events,))
    worker.start()
    participants.add(ws)
    poller = select.poll()
    poller.register(ws.socket, select.POLLIN)
    poller.register(incoming_events._reader, select.POLLIN)
    try:
        while True:
            fdVsEvent = poller.poll(10000)
            for descriptor, Event in fdVsEvent:
                if ws.socket.fileno() is descriptor:
                    m = ws.wait()
                    if m is None:
                        break
                    for p in participants:
                        p.send(m)
                else:
                    m = incoming_events.get()
                    for p in participants:
                        p.send(m)
    finally:
        participants.remove(ws)
        worker.do_run = False
        worker.join()
