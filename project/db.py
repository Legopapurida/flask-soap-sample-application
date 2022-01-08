from typing import _S, Generic, _T, Type
from flask import Flask


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

        