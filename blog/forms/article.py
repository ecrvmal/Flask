from wtforms import StringField, validators, PasswordField, SubmitField, IntegerField, BooleanField, TextAreaField, \
    SelectMultipleField
from flask_wtf import FlaskForm


class CreateArticleForm(FlaskForm):
    title = StringField('Title', [validators.DataRequired(),])
    text = TextAreaField('Text',)
    tags = SelectMultipleField('Tags', coerce=int)
    submit = SubmitField('Create')

