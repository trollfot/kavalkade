import logging
from horseman.mapping import Mapping
from minicli import cli, run


def create_web_app():
    from kavalkade.app import Kavalkade
    from kavalkade.services.clock import Clock
    from kavalkade.services.fswatcher import FileSystemWatcher
    from kavalkade import controllers, models
    from tinydb.storages import MemoryStorage
    from tinydb import TinyDB

    db = TinyDB(storage=MemoryStorage)
    app = Kavalkade(
        db,
        models=models.models,
        router=controllers.router
    )
    app.services.add(
        'clock', Clock(app.websockets))
    app.services.add(
        'fswatcher', FileSystemWatcher(['/tmp'], app.websockets))
    return app


@cli
def http(debug: bool = False):
    import sys
    from eventlet import wsgi
    from kavalkade.controllers.gamemaster import websocket_chat
    import eventlet

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
        '/chat': websocket_chat(app.websockets)
    })

    app.services.start()
    wsgi.server(
        eventlet.listen(('', 8000)),
        root,
        log=logging.getLogger('server')
    )


if __name__ == '__main__':
    run()
