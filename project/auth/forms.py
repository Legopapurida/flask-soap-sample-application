from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import EmailField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError


from .. import db 

class LoginForm(FlaskForm):

    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=18), ])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):

    username = StringField('username', validators=[DataRequired(), Length(min=3)])
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=18)])
    confirm_password = PasswordField('confirm password', validators=[EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username: StringField):
        user_id = db.connection.execute("SELECT id FROM users WHERE username=?", (username.data, ))
        if user_id: 
            raise ValidationError(message=f"Username {username.data} is already registered.")

    def validate_email(self, email: EmailField):
        user_id = db.connection.execute("SELECT id FROM users WHERE email=?", (email.data, ))
        if user_id: 
            raise ValidationError(message=f"Email {email.data} is already registered.")
