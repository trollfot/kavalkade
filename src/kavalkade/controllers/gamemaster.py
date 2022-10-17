from kavalkade.controllers import router
from knappe.decorators import html


@router.register('/talk')
@html('websocket')
def gamemaster_chat(ws):
    return {}
