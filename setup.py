from setuptools import setup


setup(
    name='kavalkade',
    install_requires=[
        'colander',
        'deform',
        'discord.py[voice]',
        'horseman',
        'knappe',
        'knappe_deform',
        'orjson',
        'pydantic',
    ],
    extras_require={
        'test': [
            'WebTest',
            'pytest',
            'pyhamcrest'
        ]
    }
)
