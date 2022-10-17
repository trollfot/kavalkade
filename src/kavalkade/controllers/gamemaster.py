from kavalkade.controllers import router
from knappe.decorators import html
from kavalkade.app import Websockets


@router.register('/talk')
@html('websocket')
def gamemaster_chat(request):
    return {}
