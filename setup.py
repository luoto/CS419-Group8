import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'curse-db',
    version = '0.0.1',
    url = 'https://github.com/LAnderson8899/CS419-Group8',
    author = 'Tony Luo <luoto@onid.oregonstate.edu>, Kristin Swanson, Leonard Anderson',
    description = 'Curse based UI for interacting with MySQL and/or PostgreSQL',
    long_description = read('README.md'),
    license = 'MIT',
    keywords = 'curses postgres mysql db',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console :: Curses',
        'Topic :: Utilities'
    ],
    install_requires = [
        'psycopg2',
        'mysql-python'
    ]
)
