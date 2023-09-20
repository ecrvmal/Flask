from flask import Blueprint, render_template, redirect
from flask_login import login_required
from werkzeug.exceptions import NotFound

from blog.models import User, Article, Author


author = Blueprint('author', __name__, url_prefix='/authors',static_folder='../static')


@author.route('/')
# @login_required
def author_list():

    """
    The author_list function renders the authors/list.html template,
        passing in a list of all Author objects from the database.

    :return: A list of all authors in our database
    :doc-author: Trelent
    """
    authors = Author.query.all()
    return render_template(
        'authors/list.html',
        authors=authors,
    )


