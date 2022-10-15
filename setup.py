from setuptools import setup


setup(
    name='kavalkade',
    install_requires=[
        'colander',
        'deform',
        'discord.py[voice]',
        'eventlet',
        'horseman',
        'knappe',
        'knappe_deform',
        'orjson',
        'pydantic',
        'tinydb',
        #'inotifyx-py3'
    ],
    extras_require={
        'test': [
            'WebTest',
            'pytest',
            'pyhamcrest'
        ]
    }
)
