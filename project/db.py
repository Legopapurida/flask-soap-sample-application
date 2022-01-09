from typing import  Generic
from typing import  TypeVar
from flask import Flask
from psycopg import Connection as PostgreSqlConnection
from sqlite3 import Connection as SqliteConnection
from sqlite3 import connect as sqlite3_connector
from psycopg import connect as psycopg_connector

_T = TypeVar('_T')
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


SqliteConnector = sqlite3_connector 
PostgreSqlConnector = psycopg_connector 