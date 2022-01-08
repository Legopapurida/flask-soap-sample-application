from flask import Flask
from .config import BaseConfig
from .db import Database
from psycopg import connect
from psycopg import Connection
from psycopg.rows import dict_row
from flask_wtf.csrf import CSRFProtect

csrf: CSRFProtect = CSRFProtect()
db: Database[Connection] = Database() 

def create_app(config:BaseConfig) -> Flask: 

    # Creating Application
    app: Flask = Flask(__name__)

    # Config application 
    app.config.from_object(config)
    
    # Creating database app
    db.connect(connection=connect(
        f"dbname={app.config['DBNAME']}"
        f"user={app.config['DBUSER']}"
        f"host={app.config['DBHOST']}"
        f"port={app.config['DBPORT']}",
        row_factory=dict_row
    ))
    db.init_app(app=app)
    
    csrf.init_app(app=app)
    return app


