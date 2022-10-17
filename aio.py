import logging
from horseman.mapping import Mapping
from minicli import cli, run


def create_web_app():
    from kavalkade.app import Kavalkade
    from kavalkade.services.clock import Clock
    from kavalkade import controllers, models
    from tinydb.storages import MemoryStorage
    from tinydb import TinyDB

    db = TinyDB(storage=MemoryStorage)
    app = Kavalkade(
        db,
        models=models.models,
        router=controllers.router
    )
    app.services.add('clock', Clock(app.websockets))
    return app


import asyncio


async def clock_x_seconds(timeout, app):
    while True:
        await asyncio.sleep(timeout)
        print(app.websockets)


import websockets

def ws_handler(connected):
    async def handler(websocket):
        import pdb
        pdb.set_trace()
        connected.add(websocket)
        try:
            while True:
                message = await websocket.recv()
                print(message)
        finally:
            connected.remove(websocket)
    return handler


async def serve_ws(connected):
    async with websockets.serve(ws_handler(connected), "", 8001):
        await asyncio.Future()  # run forever


@cli
def http(debug: bool = False):
    import sys
    import asyncio
    from aiowsgi import create_server

    log_level = logging.DEBUG if debug else logging.WARNING
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[stream_handler]
    )

    app = create_web_app()
    root = Mapping({
        '/': app,
    })

    loop = asyncio.new_event_loop()
    loop.create_task(clock_x_seconds(1, app))
    loop.create_task(serve_ws(app.websockets))
    srv = create_server(root, loop=loop, port=8000)
    srv.run()

if __name__ == '__main__':
    run()
