from flask import Flask
from flask import g
from flask import current_app

from .config import BaseConfig
from .config import DevelopmentConfig

from .db import Database
from .db import init_db

from mysql.connector import connect
from mysql.connector import MySQLConnection

from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication



csrf: CSRFProtect = CSRFProtect()
db: Database[MySQLConnection] = Database() 

#connection pool
def get_db() -> Database[MySQLConnection]:
    if 'db' not in g:
        db.connect(connect(
                host=current_app.config['DBHOST'],
                port=current_app.config['DBPORT'],
                database=current_app.config['DBNAME'],
                password=current_app.config['DBPASS'],
                user=current_app.config['DBUSER'],
            )
        )
        g.db = db

    return g.db

def create_app(config:BaseConfig=None) -> Flask: 

    # Creating Application
    app: Flask = Flask(__name__)

    # Config application 
    app.config.from_object(config or DevelopmentConfig)
    
    # Creating database app
    try:
        db.connect(connection=connect(
            host=app.config['DBHOST'],
            port=app.config['DBPORT'],
            database=app.config['DBNAME'],
            password=app.config['DBPASS'],
            user=app.config['DBUSER']
        ))
    except:
        pass
    db.init_app(app=app)
    app.cli.add_command(init_db)

    csrf.init_app(app=app)

    from .auth import auth
    from .auth.middleware import load_logged_in_user
    from .services.client import site
    
    from .services.server import create_soap

    app.before_request(load_logged_in_user)
    soap_app = create_soap(app)
    #wisgi => for sync webService Mechanism
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/soap': WsgiApplication(soap_app)
    })


    #routers
    app.register_blueprint(auth)
    app.register_blueprint(site)

    #root router
    app.add_url_rule('/', endpoint='home')

    return app


