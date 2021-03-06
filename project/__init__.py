from flask import Flask
from .config import BaseConfig
from .db import Database
from .db import PostgreSqlConnection
from .db import PostgreSqlConnector
from psycopg.rows import class_row
from flask_wtf.csrf import CSRFProtect

csrf: CSRFProtect = CSRFProtect()
db: Database[PostgreSqlConnection] = Database() 


def create_app(config:BaseConfig) -> Flask: 

    # Creating Application
    app: Flask = Flask(__name__)

    # Config application 
    app.config.from_object(config)
    
    # Register Middleware
    from .middleware import load_logged_in_user
    
    app.before_request(load_logged_in_user)

    # Creating database app
    db.connect(connection=PostgreSqlConnector(
        f"dbname={app.config['DBNAME']}"
        f"user={app.config['DBUSER']}"
        f"host={app.config['DBHOST']}"
        f"port={app.config['DBPORT']}",
        row_factory=class_row
    ))
    db.init_app(app=app)
    
    csrf.init_app(app=app)
    return app


