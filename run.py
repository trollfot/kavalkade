from minicli import cli, run


def configure_logging(debug=False):
    import sys
    import logging

    log_level = logging.DEBUG if debug else logging.WARNING
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[stream_handler]
    )


def create_web_app():
    from kavalkade.app import Kavalkade
    from kavalkade import controllers, models
    from tinydb.storages import MemoryStorage
    from tinydb import TinyDB

    db = TinyDB(storage=MemoryStorage)
    app = Kavalkade(
        TinyDB(storage=MemoryStorage),
        models=models.models,
        router=controllers.router,
        websockets=controllers.websockets,
    )
    return app


@cli
def http(debug: bool = False):
    import asyncio
    from aiowsgi import create_server
    from kavalkade.services.fswatcher import fswatcher
    from kavalkade.services.clock import clock

    configure_logging(debug)

    app = create_web_app()
    loop = asyncio.new_event_loop()
    app.services.bind(loop)
    app.services.add('clock', clock(app, 3))
    app.services.add('file_watcher', fswatcher(app, '/tmp'))
    app.services.add('websockets', app.websockets.serve())
    wsgi_server = create_server(app, loop=loop, port=8000)

    try:
        app.services.start()
        wsgi_server.run()
    except:
        loop.run_until_complete(app.services.stop())
    finally:
        loop.stop()


if __name__ == '__main__':
    run()
