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
    import aioftp
    import pathlib
    from aiowsgi import create_server
    from kavalkade.services.fswatcher import fswatcher
    from kavalkade.services.clock import clock, services_status

    configure_logging(debug)

    root = pathlib.Path(__file__).parent / 'ftproot'
    users = [
        aioftp.User(
            "test",
            "test",
            home_path='/ftproot/test',
            permissions=(
                aioftp.Permission("/", readable=False, writable=False),
                aioftp.Permission('/ftproot/test', readable=True, writable=True),
            )
        )
    ]

    app = create_web_app()
    loop = asyncio.new_event_loop()
    app.services.bind(loop)
    app.services.add('clock', clock(app, 3))
    app.services.add('statuses', services_status(app, 10))
    app.services.add('file_watcher', fswatcher(app, '/tmp'))
    app.services.add('websockets', app.websockets.serve())
    app.services.add('ftp', aioftp.Server(users=users).start(port=8021))
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
