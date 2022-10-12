from knappe.meta import HTTPMethodEndpointMeta
from knappe.decorators import html

class Index(metaclass=HTTPMethodEndpointMeta):

    @html('index')
    def GET(self, request):
        return {}
    