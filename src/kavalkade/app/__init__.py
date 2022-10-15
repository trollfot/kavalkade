import typing as t
from dataclasses import dataclass, field
from tinydb import TinyDB
from horseman.mapping import RootNode
from knappe.blueprint import Blueprint
from knappe.pipeline import Pipeline
from knappe.request import RoutingRequest as Request
from knappe.response import Response
from knappe.routing import Router
from knappe.types import Middleware
from .ui import ui
from .models import Models
from .services import Services

class Websockets(set):

    def broadcast(self, message: str):
        for ws in self:
            ws.send(message)

    def broadcast_from(self, origin, message):
        for ws in self:
            if ws is not origin:
                ws.send(message)


@dataclass
class Kavalkade(RootNode):
    database: TinyDB
    websockets: Websockets = field(default_factory=Websockets)
    models: Models = field(default_factory=Models)
    router: Router = field(default_factory=Router)
    services: Services = field(default_factory=Services)
    middlewares: t.Iterable[Middleware] = field(default_factory=tuple)

    def __post_init__(self, middlewares=()):
        self.pipeline: Pipeline[Request, Response] = Pipeline(
            self.middlewares
        )

    def resolve(self, path, environ):
        endpoint = self.router.match_method(path, environ['REQUEST_METHOD'])
        return self.pipeline(endpoint.handler)(
            Request(
                environ,
                app=self,
                endpoint=endpoint,
                context={"ui": ui}
            )
        )
