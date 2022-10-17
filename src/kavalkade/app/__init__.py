import asyncio
import typing as t
import websockets
from autoroutes import Routes
from dataclasses import dataclass, field
from tinydb import TinyDB
from horseman.mapping import RootNode
from knappe.pipeline import Pipeline
from knappe.request import RoutingRequest as Request
from knappe.response import Response
from knappe.routing import Router
from knappe.types import Middleware
from .ui import ui
from .models import Models
from .services import Services


WebsocketHandler = t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]]


class Websockets:

    def __init__(self, handlers: t.Optional[Routes] = None):
        if handlers is None:
            handlers = Routes()
        self.handlers = handlers
        self.connected = set()
        self.app = None

    def bind(self, app):
        self.app = app

    async def broadcast(self, message: str):
        for ws in self.connected:
            await ws.send(message)

    async def broadcast_from(self, origin, message):
        for ws in self.connected:
            if ws is not origin:
                await ws.send(message)

    def register(self, path):
        def register_handler(coro: WebsocketHandler):
            print('I register path for ', coro)
            self.handlers.add(path, handler=coro)
            return coro
        return register_handler

    async def handler(self, ws):
        payload, params = self.handlers.match(ws.path)
        if not payload:
            raise RuntimeError('Could not find a ws handler.')
        handler: WebsocketHandler = payload['handler']
        try:
            self.connected.add(ws)
            await handler(self.app, ws, **params)
        except websockets.exceptions.ConnectionClosedOK:
            pass
        finally:
            self.connected.remove(ws)

    async def serve(self, port: int = 8001):
        async with websockets.serve(self.handler, "", port):
            await asyncio.Future()  # run forever


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
        self.websockets.bind(self)

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
