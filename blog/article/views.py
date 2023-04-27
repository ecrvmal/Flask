from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import NotFound

from blog.models import User, Article, Author
from blog.extensions import db
from blog.forms.article import CreateArticleForm




article = Blueprint('article', __name__, url_prefix='/articles',static_folder='../static')


# key_list = ['id', 'title', 'text', 'a_user_id', ]

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
def article_details(pk: int):
    the_article = Article.query.filter_by(id=pk).one_or_none()
    # users = User.query.all()
    if not the_article:
        raise NotFound(f"Article #{pk} doesn't exist!")
    return render_template(
        'articles/details.html',
        article=the_article,
    )


@article.route('/create', methods=['GET',"POST"])
@login_required
def create_article():
    if request.method == 'GET':
        form = CreateArticleForm(request.form)
        return render_template('articles/create.html', form=form)

    if request.method == 'POST':
        form = CreateArticleForm(request.form)
        if form.validate_on_submit():
            if current_user.author:
                _author = current_user.author.id
            else:
                author = Author(user_id=current_user.id)
                db.session.add(author)
                db.session.flush()
                _author = author.id
            _article = Article(title=form.title.data.strip(), text=form.text.data, author_id=_author)

            db.session.add(_article)
            db.session.commit()

            return redirect(url_for('article.article_details', pk=_article.id))

        return render_template(
            'articles/create.html',
            form=form,
    )


