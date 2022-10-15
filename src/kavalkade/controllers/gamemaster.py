from eventlet import websocket
from kavalkade.controllers import router
from knappe.decorators import html
from kavalkade.app import Websockets


@router.register('/talk')
@html('websocket')
def gamemaster_chat(request):
    return {}


def websocket_chat(registry: Websockets):

    @websocket.WebSocketWSGI
    def chat(ws: websocket.WebSocket):
        registry.add(ws)
        try:
            while True:
                m = ws.wait()
                if m is None:
                    break
                registry.broadcast(m)
        finally:
            registry.remove(ws)

    return chat
