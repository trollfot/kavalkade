from setuptools import setup


setup(
    name='kavalkade',
    install_requires=[
        'colander',
        'deform',
        'discord.py[voice]',
        'horseman',
        'inotipy',
        'knappe',
        'knappe_deform',
        'orjson',
        'pydantic',
        'tinydb',
        'aiowsgi',
    ],
    extras_require={
        'test': [
            'WebTest',
            'pytest',
            'pyhamcrest'
        ]
    }
)
