from flask import Blueprint, render_template, redirect
from blog.user.views import USERS
from werkzeug.exceptions import NotFound


article = Blueprint('article', __name__, url_prefix='/articles',static_folder='../static')

ARTICLES = {
    1: {'title': '1_Notes to Congress', 'author': 2, 'text':'1_Here is a long text with notes to Congress'},
    2: {'title': '2_Speech to Citizens', 'author': 1, 'text': '2_Here is a long speech to Citizens'},
    3: {'title': '3_About Life in USA ', 'author': 3, 'text': '3_Here is a long article About Life in USA'},
    4: {'title': '4_Help to Hospitals', 'author': 2, 'text': '4_Here is a long article about Help to Hospitals'},
    5: {'title': '5_The origin of COVID', 'author': 1, 'text': '5_Here is a long article about The origin of COVID'},
    6: {'title': '6_How to decrease unemployment', 'author': 4, 'text': '6_Here is a long article about How to decrease unemployment'},
}


@article.route('/')
def article_list():
    for item in ARTICLES:
        key_list=list(ARTICLES[item])
    return render_template(
        'articles/list.html',
        articles=ARTICLES,
        key_list=key_list,
        users=USERS
    )

@article.route('/<int:pk>')
def get_article(pk: int):
    try:
        the_article = ARTICLES[pk]
    except KeyError:
        # raise NotFound(f'user id {pk} not found')      # change error message
        return redirect('/articles/')                       # or make action  (redirect) on error
    key_list = list(the_article)
    return render_template(
        'articles/details.html',
        article=the_article,
        key_list=key_list,
        id=pk,
        users=USERS,
    )


