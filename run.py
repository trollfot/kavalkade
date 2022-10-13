import logging
import contextlib
from minicli import cli, run


@contextlib.contextmanager
def temporary_app():
    from kavalkade.app import Kavalkade
    from kavalkade import controllers, models
    from tinydb import TinyDB

    db = TinyDB('test.json')
    try:
        yield Kavalkade(db, models=models.models, router=controllers.router)
    finally:
        logging.warning('Cleaning DB entirely.')
        db.drop_tables()


@cli
def http(debug: bool = False):
    import sys
    import bjoern

    log_level = logging.DEBUG if debug else logging.WARNING
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[stream_handler]
    )
    with temporary_app() as app:
        logging.info(f'Server starts with {app}.')
        bjoern.run(app, "127.0.0.1", 8000)


if __name__ == '__main__':
    run()
