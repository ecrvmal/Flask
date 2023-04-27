from flask import Blueprint, render_template, redirect
from flask_login import login_required
from werkzeug.exceptions import NotFound




user = Blueprint('user', __name__,url_prefix='/users',static_folder='../static')


# USERS = {
#     1: {'first_name': 'Joe','last_name':'Biden','birth_year':1942},
#     2: {'first_name': 'Donald', 'last_name':'Trump', 'birth_year':1946},
#     3: {'first_name': 'Barack', 'last_name':'Obama', 'birth_year':1961},
#     4: {'first_name': 'George', 'last_name':'Bush jr', 'birth_year':1946},
#     5: {'first_name': 'Bill', 'last_name':'Klinton', 'birth_year':1946},
#     6: {'first_name': 'Ronald', 'last_name':'Reagan', 'birth_year':1911},
#     }

@user.route('/')
@login_required
def user_list():
    from blog.models import User
    users = User.query.all()
    key_list = ['id', 'username', 'email', ]
    return render_template(
        'users/list.html',
        users=users,
        key_list=key_list,
    )


@user.route('/<int:pk>')
@login_required
def user_details(pk: int):

    from blog.models import User
    _user = User.query.filter_by(id=pk).one_or_none()
    key_list = ['id', 'username', 'email', ]
    if not _user:
        # raise NotFound(f'user id {pk} not found')      # change error message
        return redirect('/users/')                       # or make action  (redirect) on error
    return render_template(
        'users/details.html',
        id=pk,
        user=_user,
        key_list=key_list
    )


