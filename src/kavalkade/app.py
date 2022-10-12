from horseman.mapping import RootNode
from knappe.request import RoutingRequest as Request
from knappe.response import Response
from knappe.pipeline import Pipeline

from .views import ui
from .routes import router

class Kavalkade(RootNode):
    def __init__(self, router=router, config=None):
        self.config = config
        self.router = router
        self.pipeline: Pipeline[Request, Response] = Pipeline(())

    def resolve(self, path, environ):
        endpoint = self.router.match_method(path, environ['REQUEST_METHOD'])
        return self.pipeline(endpoint.handler)(
            Request(
                environ, 
                app=self, 
                endpoint=endpoint,
                context={"ui" : ui}
            )
        )