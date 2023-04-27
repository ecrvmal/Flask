from flask import Blueprint, render_template, redirect
from flask_login import login_required
from werkzeug.exceptions import NotFound

from blog.models import User, Article



article = Blueprint('article', __name__, url_prefix='/articles',static_folder='../static')

key_list = ['id', 'title', 'text', 'a_user_id', ]

# ARTICLES = {
#     1: {'title': '1_Notes to Congress', 'author': 2, 'text':'1_Here is a long text with notes to Congress'},
#     2: {'title': '2_Speech to Citizens', 'author': 1, 'text': '2_Here is a long speech to Citizens'},
#     3: {'title': '3_About Life in USA ', 'author': 3, 'text': '3_Here is a long article About Life in USA'},
#     4: {'title': '4_Help to Hospitals', 'author': 2, 'text': '4_Here is a long article about Help to Hospitals'},
#     5: {'title': '5_The origin of COVID', 'author': 1, 'text': '5_Here is a long article about The origin of COVID'},
#     6: {'title': '6_How to decrease unemployment', 'author': 4, 'text': '6_Here is a long article about How to decrease unemployment'},
# }


@article.route('/')
@login_required
def article_list():
    articles = Article.query.all()
    users = User.query.all()
    return render_template(
        'articles/list.html',
        articles=articles,
        users=users
    )

@article.route('/<int:pk>')
@login_required
def get_article(pk: int):
    the_article = Article.query.filter_by(id=pk).one_or_none()
    # users = User.query.all()
    if not the_article:
        raise NotFound(f"Article #{pk} doesn't exist!")
    author = User.query.filter_by(id=the_article.id).one_or_none()

    return render_template(
        'articles/details.html',
        article=the_article,
        key_list=key_list,
        id=pk,
        author=author,
    )


