from flask import Blueprint, render_template, redirect
from werkzeug.exceptions import NotFound




user = Blueprint('user', __name__,url_prefix='/users',static_folder='../static')

USERS = {
    1: {'first_name': 'Joe','last_name':'Biden','birth_year':1942},
    2: {'first_name': 'Donald', 'last_name':'Trump', 'birth_year':1946},
    3: {'first_name': 'Barack', 'last_name':'Obama', 'birth_year':1961},
    4: {'first_name': 'George', 'last_name':'Bush jr', 'birth_year':1946},
    5: {'first_name': 'Bill', 'last_name':'Klinton', 'birth_year':1946},
    6: {'first_name': 'Ronald', 'last_name':'Reagan', 'birth_year':1911},
    }

@user.route('/')
def user_list():
    for item in USERS:
        key_list = list(USERS[item])
    return render_template(
        'users/list.html',
        users=USERS,
        key_list=key_list
    )


@user.route('/<int:pk>')
def get_user(pk: int):
    try:
        user_item = USERS[pk]
    except KeyError:
        return redirect('/users/')
    key_list = list(USERS[pk])
    return render_template(
        'users/details.html',
        id=pk,
        user=user_item,
        key_list=key_list
    )


