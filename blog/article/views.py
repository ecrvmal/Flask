
import codecs
import urllib.request
import json

import requests
from flask import Blueprint, render_template, redirect, request, url_for, json
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.configs import API_URL
from blog.models import User, Article, Author, Tag
from blog.extensions import db
from blog.forms.article import CreateArticleForm


article = Blueprint('article', __name__, url_prefix='/articles', static_folder='../static')

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
    """
    The article_list function renders the article_list.html template,
    which displays all articles in the database.

    :return: A rendered template of the articles/list
    :doc-author: Trelent
    """
    articles = Article.query.all()
    users = User.query.all()
    return render_template(
        'articles/list.html',
        articles=articles,
        users=users,
    )


@article.route('/<int:pk>')
@login_required
def article_details(pk: int):
    """
    The article_details function will be used to display the details of a single article.
    It will accept an integer primary key (pk) as its only argument, and it will return a rendered template.
    The template should be named 'articles/details.html'. The context for this template should contain one variable:
    article, which is the Article object that corresponds to the pk passed in.

    :param pk: int: Pass in the primary key of an article
    :return: A rendered template
    """
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
    """
    The create_article function is responsible for creating a new article.
    It will first check if the request method is GET or POST. If it's GET, then we'll render the create template with an empty form.
    If it's POST, then we'll validate the form and save our new article to the database.

    :return: A redirect to the article_details function
    """
    if request.method == 'GET':
        form = CreateArticleForm(request.form)
        form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
        return render_template('articles/create.html', form=form)

    if request.method == 'POST':
        form = CreateArticleForm(request.form)
        form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by('name')]
        if form.validate_on_submit():
            if current_user.author:
                _author = current_user.author.id
            else:
                author = Author(user_id=current_user.id)
                db.session.add(author)
                db.session.flush()
                _author = author.id
            _article = Article(title=form.title.data.strip(), text=form.text.data, author_id=_author)

            if form.tags.data:
                selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
                for tag in selected_tags:
                    _article.tags.append(tag)

            db.session.add(_article)
            db.session.commit()

            return redirect(url_for('article.article_details', pk=_article.id))

        return render_template(
            'articles/create.html',
            form=form,
    )


@article.route('/tag/<int:pk>')
@login_required
def article_tag_details(pk: int):

    """
    The article_tag_details function is a route that takes in an integer primary key (pk) and returns the details of all articles with the tag associated with that pk.

    :param pk: int: Specify the primary key of the tag that we want to display
    :return: The rendered template for the article_set
    """
    selected_tag = Tag.query.filter_by(id=pk).one_or_none()

    article_set = Article.query.options(joinedload(Article.tags)).filter(Article.tags.any(Tag.id == pk))
    if not article_set:
        raise NotFound(f"Article with tag #{pk} doesn't exist!")
    return render_template(
        'articles/article_set.html',
        article_set=article_set,
        selected_tag=selected_tag,
    )


@article.route('/api')
# @login_required
def article_api_list():

    """
    The article_api_list function is a route that renders the article_api.html template, which displays all articles in the database.
    The function uses requests to get data from an API endpoint and then loads it into a dictionary using json.loads().
    It then passes this dictionary as an argument to render_template().

    :return: A list of articles from the api
    :doc-author: Trelent
    """
    article_set = requests.get(f'{API_URL}/api/articles')
    # article_set = requests.get(f'{API_URL}/api/articles/event_get_list')
    # article_set = requests.get('https://flask-api-deployment-cr01.onrender.com/api/articles')
    if not article_set:
        raise NotFound(f"Article list is empty!")
    article_dict = json.loads(article_set.content)
    # article_data = article_dict["list"]["data"]
    article_data = article_dict["data"]
    return render_template(
        'articles/article_api.html',
        article_list=article_data,
    )



