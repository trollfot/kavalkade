from knappe.routing import Router
from autoroutes import Routes
from kavalkade.app import Websockets


router = Router()
websockets = Websockets()


from . import profile, models, index, character, gamemaster, wshandlers
