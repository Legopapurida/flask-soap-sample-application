from flask import Flask
from flask import current_app
from flask import request
from flask import g
from flask import abort
from flask.helpers import make_response
from flask.templating import render_template
from .config import BaseConfig
from .config import DevelopmentConfig
from .db import Database
from .db import init_db
# from mysql.connector import connect
# from mysql.connector import MySQLConnection
from sqlite3 import connect
from sqlite3 import Connection
from sqlite3 import Row
from sqlite3 import PARSE_DECLTYPES
from flask_wtf.csrf import CSRFProtect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication
import requests

from zeep.client import Client

csrf: CSRFProtect = CSRFProtect()
db: Database[Connection] = Database() 

def get_db() -> Database[Connection]:
    if 'db' not in g:
        db.connect(connect(
                'site.db',
                detect_types=PARSE_DECLTYPES
            )
        )
        db.connection.row_factory = Row
        g.db = db
        g.db.row_factory = Row

    return g.db

def create_app(config:BaseConfig=None) -> Flask: 

    # Creating Application
    app: Flask = Flask(__name__)

    # Config application 
    app.config.from_object(config or DevelopmentConfig)
    
    # Creating database app
    # db.connect(connection=connect(
    #     host=app.config['DBHOST'],
    #     port=app.config['DBPORT'],
    #     database=app.confif['DBNAME'],
    #     password=app.config['DBPASS'],
    #     username=app.config['DBUSER']
    # ))
    db.connect(connection=connect('site.db', detect_types=PARSE_DECLTYPES))
    db.connection.row_factory = Row
    db.init_app(app=app)
    app.cli.add_command(init_db)

    csrf.init_app(app=app)

    from .auth import auth
    from .auth.controllers import login_required
    from .services.server import FininceService
    from .services.server import create_soap

    soap_app = create_soap(app)
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/soap': WsgiApplication(soap_app)
    })

    @app.route('/')
    @app.route('/home')
    @app.route('/index')
    @login_required
    def index():
        url = request.host_url + '/soap/get_debt?wsdl'
        cl = Client(url)
        debt = cl.service.get_debt(1)
        if not debt:
            debt = g.user.debt
        return render_template('index.html', debt = debt)

    
    app.register_blueprint(auth)
    app.add_url_rule('/', endpoint='home')
    return app


