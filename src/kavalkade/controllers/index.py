from knappe.meta import HTTPMethodEndpointMeta
from knappe.decorators import html
from kavalkade.controllers import router


@router.register('/')
class Index(metaclass=HTTPMethodEndpointMeta):

    @html('index')
    def GET(self, request):
        request.app.websockets.sync_broadcast('Someone asked for the index')
        return {'request': request}
