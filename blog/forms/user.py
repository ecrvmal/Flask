from wtforms import StringField, validators, PasswordField, SubmitField, IntegerField, BooleanField
from flask_wtf import FlaskForm


class UserLoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')


class UserRegisterForm(FlaskForm):
    username = StringField('Username')
    email = StringField('E-mail', [validators.DataRequired(),
                                   validators.Email()])
    # birth_year = IntegerField('Birth Year')

    is_staff = BooleanField('Is Staff')
    password = PasswordField('Password', [
        validators.DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     [validators.DataRequired(),
                                      validators.EqualTo('password',
                                                         message='Field must be equal to password')])
    submit = SubmitField('Register')

