from minicli import cli, run
import logging


def create_web_app(**common):
    from kavalkade.app import Kavalkade
    from kavalkade import controllers, models
    from tinydb.storages import MemoryStorage
    from tinydb import TinyDB

    db = TinyDB(storage=MemoryStorage)
    app = Kavalkade(
        db,
        models=models.models,
        router=controllers.router,
        websockets=controllers.websockets,
    )
    return app


@cli
def http(debug: bool = False):
    import sys
    import asyncio
    from aiowsgi import create_server
    from kavalkade.services.fswatcher import fswatcher
    from kavalkade.services.clock import clock

    log_level = logging.DEBUG if debug else logging.WARNING
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[stream_handler]
    )

    app = create_web_app()

    loop = asyncio.new_event_loop()
    app.services.bind(loop)
    app.services.add('clock', clock(app, 3))
    app.services.add('file_watcher', fswatcher(app, '/tmp'))
    app.services.add('websockets', app.websockets.serve())
    app.services.start()

    srv = create_server(app, loop=loop, port=8000)
    srv.run()

if __name__ == '__main__':
    run()
