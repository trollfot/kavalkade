from eventlet import websocket
from kavalkade.controllers import router
from knappe.decorators import html


participants = set()


@router.register('/talk')
@html('websocket')
def gamemaster_chat(ws):
    return {}


@websocket.WebSocketWSGI
def chat(ws):
    participants.add(ws)
    try:
        while True:
            m = ws.wait()
            if m is None:
                break
            for p in participants:
                p.send(m)
    finally:
        participants.remove(ws)
