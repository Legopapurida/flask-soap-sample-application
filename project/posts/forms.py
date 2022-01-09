from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):

    title = StringField('title', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdatePostForm(FlaskForm):

    title = StringField('title', validators=[DataRequired()])
    body = TextAreaField('body', validators=[DataRequired()])
    submit = SubmitField('Update')