from flask import session
from flask import g
from mysql.connector.cursor import MySQLCursor

from .. import get_db
from . import auth
from .models import User

def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cursor: MySQLCursor = get_db().connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE id = %s ", (user_id, )
            )
        g.user = User(**cursor.fetchone()
        )