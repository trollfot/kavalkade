from minicli import cli, run


def create_app():
    from kavalkade.app import Kavalkade
    from kavalkade import controllers, models

    return Kavalkade(models=models.models, router=controllers.router)


@cli
def http(debug: bool = False):
    import sys
    import logging
    import bjoern

    log_level = logging.DEBUG if debug else logging.WARNING
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[stream_handler]
    )
    app = create_app()
    logging.info('Server starts.')
    bjoern.run(app, "127.0.0.1", 8000)


if __name__ == '__main__':
    run()
