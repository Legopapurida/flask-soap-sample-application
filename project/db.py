from typing import  Generic, Type, TypeVar
from flask import Flask
from flask import current_app
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
    from mysql.connector import connect
    from mysql.connector import MySQLConnection
    from mysql.connector.cursor import MySQLCursor
    with open('project/db.sql', 'r') as f:
        db: Database[MySQLConnection] = Database()
        db.connect(connect(host=current_app.config['DBHOST'],
            port=current_app.config['DBPORT'],
            password=current_app.config['DBPASS'],
            user=current_app.config['DBUSER']
        ))
        curs: MySQLCursor = db.connection.cursor()
        curs.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
        for line in f.readlines():
            curs.execute(line)