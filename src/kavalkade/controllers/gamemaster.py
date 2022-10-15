from eventlet import websocket
from kavalkade.controllers import router
from knappe.decorators import html


@router.register('/talk')
@html('websocket')
def gamemaster_chat(ws):
    return {}


def websocket_chat(registry):

    @websocket.WebSocketWSGI
    def chat(ws):
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