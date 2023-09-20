from sqlite3 import IntegrityError

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import logout_user, login_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from blog.models import User
from blog.extensions import db
from blog.forms.user import UserLoginForm
from blog.forms.user import UserRegisterForm

auth = Blueprint('auth', __name__, static_folder='../static')

@auth.route('/')
def hello():
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=('GET', 'POST'))
def login():
    """
    The login function is responsible for rendering the login page and handling
    the POST request from the login form. It uses Flask-Login's `login_user` function
    to log in a user, which sets up session variables to track that a user is logged in.


    :return: A redirect to the user list page
    :doc-author: Trelent
    """
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('user.user_details', pk=current_user.id))
            # return redirect(url_for('user.user_list'))

    errors = []
    form = UserLoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            form.password.errors.append("Please check username and password")
            flash('Check your login details')
            # return redirect(url_for('auth.login'))
            return render_template('auth/login.html', form=form)

        login_user(user)
        return redirect(url_for('user.user_list'))
    return render_template(
        'auth/login.html',
        form=form,
        errors=errors,
    )


@auth.route('/register', methods=('GET', 'POST'))
def register():
    """
    The register function is responsible for registering a new user.
    It will validate the form, and if it is valid, create a new User object and add it to the database.
    If there are any errors in validation or adding to the database, they will be stored in an error list which will be passed into our template.

    :return: A redirect to the user list
    """
    if current_user.is_authenticated:
        return redirect(url_for('user.get_user', pk=current_user.id))

    errors = []
    form = UserRegisterForm(request.form)  # request.form - If there is a value for key,
    # the form  will display the value after page reload
    # this need for debugging
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():  # User is model
            form.email.errors.append("email isn't uniq")
            return render_template('users/register.html', form=form)
        if User.query.filter_by(username=form.username.data).count():  # User is model
            form.username.errors.append("username isn't uniq")
            return render_template('users/register.html', form=form)

        _user = User(
            username=form.username.data,
            email=form.email.data,
            # birth_year=form.birth_year.data,
            is_staff=False,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(_user)
        try:
            db.session.commit()
        except IntegrityError:
            errors.append("Database Commit Error")
        else:
            login_user(_user)
        return redirect(url_for('user.user_list'))

    return render_template(
        'auth/register.html',
        form=form,
        errors=errors
    )


@auth.route('/logout')
@login_required
def logout():
    """
    The logout function logs the user out of their account.
        It does this by calling the logout_user() function from Flask-Login, which removes all session data and cookies.

    :return: A redirect to the login page
    :doc-author: Trelent
    """
    logout_user()
    return redirect(url_for('.login'))
