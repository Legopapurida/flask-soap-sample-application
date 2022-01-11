from flask import request
from flask import flash
from flask import g
from flask import session
from flask import abort
from flask import redirect
from flask import url_for
from flask import render_template
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from .. import get_db

from . import auth
from .forms import SignUpForm
from .forms import LoginForm
from .models import User
from .controllers import login_required


from random import randint



@auth.route('/login', methods=['GET', 'POST'])
def login():

    form: LoginForm = LoginForm()

    if g.user:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # cursor: MySQLCursor = db.connection.cursor(dictionary=True)
        cursor = get_db().connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
                (
                    form.email.data,
                )
            )
        finded = cursor.fetchone()
        if finded:
            user: User = User(**finded)
            if check_password_hash(user.password, form.password.data):
                flash('You logged in successfully!', 'success')
                session['user_id'] = user.id
                return redirect(url_for('index'))
        else:
            flash('There is some wrong, please check ', 'danger')    
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    flash('you logged out successfully')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    form: SignUpForm = SignUpForm()
    contexts: dict = dict(
        form=form, 
        title='Sign Up', 
    )
    if form.validate_on_submit():
        # cursor: MySQLCursor = db.connection.cursor(dictionary=True)
        cursor = get_db().connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password, fname, lname, address, debt) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (
                        form.username.data,
                        form.email.data,
                        generate_password_hash(form.password.data), 
                        form.fname.data,
                        form.lname.data,
                        form.address.data,
                        randint(1000000, 1000000000)
                    )
                )
        flash("You signed up successfully!", 'success')
        get_db().connection.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', **contexts)
            