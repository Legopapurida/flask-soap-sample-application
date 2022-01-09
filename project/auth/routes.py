from flask import request
from flask import flash
from flask import g
from flask import session
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from psycopg.rows import class_row
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from .. import db
from ..controllers import login_required

from . import auth as router
from .forms import SignUpForm
from .forms import LoginForm
from .models import User


@router.post('/login')
async def login():

    form: LoginForm = LoginForm()
    message: str = ...
    contexts: dict = dict(
        form=form, 
        title='Login', 
    )
    if g.user:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        with db.connection.cursor(row_factory=class_row(User)) as cursor:
            try:
                user: User = cursor.execute(
                    "SELECT * FROM users WHERE email = %s",
                        (
                            form.email.data,
                        )
                    ).fetchone()
                if user and check_password_hash(user.email, form.email.data):
                    message = ('You logged in successfully!', 'success')
                    session['user_id'] = user['id']
                else:
                    message = ('There is some wrong, please check ', 'danger')    
            except Exception:
                db.connection.rollback()
                abort(500)
            else:
                return redirect(url_for('index'))
            finally:
                db.connection.close()
    flash(*message)
    return render_template('auth/login.html', **contexts)


@router.get('/logout')
@login_required
async def logout():
    session.pop('user_id')
    flash('you logged out successfully')
    return redirect(url_for('auth.login'))


@router.post('/signup')
async def signup():
    form: SignUpForm = SignUpForm()
    contexts: dict = dict(
        form=form, 
        title='Sign Up', 
    )
    if form.validate_on_submit():
        with db.connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (
                        form.username.data,
                        form.email.data,
                        generate_password_hash(form.password.data)
                    )
                )
            except Exception:
                db.connection.rollback()
                abort(500)
            else:
                flash("You signed up successfully!", 'success')
                db.connection.commit()
                return redirect(url_for('auth.login'))
            finally:
                db.connection.close()
    return render_template('auth/signup.html', **contexts)
            