from typing import  Generic, Type, TypeVar
from flask import Flask
from flask.cli import with_appcontext
import click

_T = TypeVar('_T')
_S = TypeVar('_S')


class Database(Generic[_T]):

    def __init__(self, app: Flask = None) -> None:
        self.app: Flask = app
        self.__connection: _T = ...
        if app is not None:
            self.init_app(app=app)

    def init_app(self, app: Flask) -> None:
        if self.__connection:
            self.app: Flask = app
            
        else:
            raise RuntimeError("there is not any specific connection")

    def connect(self, connection: _T) -> _T:
        self.__connection = connection

    @property
    def connection(self):
        return self.__connection


@click.command('init-db')
@with_appcontext
def init_db():
    from sqlite3 import connect
    from sqlite3 import PARSE_DECLTYPES
    from sqlite3 import Row
    with open('project/db.sql', 'r') as f:
        query = f.read()
        db = Database()
        db.connect(connection=connect('site.db', detect_types=PARSE_DECLTYPES))
        db.connection.row_factory = Row
        db.connection.execute(query)