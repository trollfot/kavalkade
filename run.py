import logging
from horseman.mapping import Mapping
from minicli import cli, run


def create_web_app():
    from kavalkade.app import Kavalkade
    from kavalkade import controllers, models
    from tinydb.storages import MemoryStorage
    from tinydb import TinyDB

    db = TinyDB(storage=MemoryStorage)
    return Kavalkade(db, models=models.models, router=controllers.router)


@cli
def http(debug: bool = False):
    import sys
    from eventlet import wsgi
    from kavalkade.controllers.gamemaster import chat
    import eventlet

    log_level = logging.DEBUG if debug else logging.WARNING
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[stream_handler]
    )

    root = Mapping({
        '/': create_web_app(),
        '/chat': chat
    })

    wsgi.server(
        eventlet.listen(('', 8000)),
        root,
        log=logging.getLogger('server')
    )


if __name__ == '__main__':
    run()
