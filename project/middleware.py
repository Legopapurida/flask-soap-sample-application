from flask import session
from flask import g

from . import db
from .auth.models import User


def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User(**db.connection.execute(
            "SELECT * FROM users WHERE id = ? ", (user_id, )
            ).fetchone()
        )