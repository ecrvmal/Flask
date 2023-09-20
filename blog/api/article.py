import requests
import json
from combojsonapi.event.resource import EventsResource
from flask import request, jsonify
from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.configs import API_URL
from blog.schemas import ArticleSchema
from blog.extensions import db
from blog.models import Article


class ArticleListEvent(EventsResource):

    def event_get_count(self, *args, **kwargs):
        """
        The event_get_count function returns the number of articles in the database.

        :param self: Access the class instance
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: The number of articles in the database
        """
        return{'count': Article.query.count()}

    def event_get_list(self, *args, **kwargs):

        """
        The event_get_list function is a Flask-SocketIO event that returns the list of articles from the API.
        The function uses requests to make a GET request to the API's /api/articles route, which returns all articles in JSON format.
        The function then sends this data back to the client using SocketIO's emit method.

        :param self: Represent the instance of the class
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: The list of articles from the api
        :doc-author: Trelent
        """
        # return{'list': requests.get('https://flask-api-deployment-cr01.onrender.com/api/articles').json()}
        return{'list': requests.get(f'{API_URL}/api/articles').json()}
        # return{'list': requests.get('http://127.0.0.1:5000/api/articles').json()}  # this works
        # return{'list': Article.query.all()}                              # this don't works
        # return{'list': Article.query.all().json()}                       # this don't works
        # article_set = json.dumps(Article.query.all())
        # return{'list': article_set}


    def event_post_count(self):
        """
        The event_post_count function is a GET request that returns the number of posts for each event.
            The function takes in an event_id and returns the count of posts associated with that id.

        :param self: Access the class attributes and methods
        :return: The http method used to make the request
        """
        return{'method': request.method}


    def event_get_api_server(self):
        """
        The event_get_api_server function is a simple function that returns the IP address of the server.
            It uses an external API to get this information.

        :param self: Represent the instance of the class
        :return: The count of the number of times it has been called
        :doc-author: Trelent
        """
        return {'count': requests.get('https://ifconfig.io/ip').text}


class ArticleDetailEvent(EventsResource):
    def event_get_count_by_author(self, *args, **kwargs):

        """
        The event_get_count_by_author function is a custom event that returns the number of articles written by a specific author.
        It takes in an id as an argument and returns the count of all articles with that author_id.

        :param self: Represent the instance of the class
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass a variable number of keyword arguments to a function
        :return: The number of articles written by a specific author
        :doc-author: Trelent
        """
        return{'count': Article.query.filter(Article.author_id == kwargs['id']).count()}


class ArticleList(ResourceList):
    events = ArticleListEvent
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }


class ArticleDetail(ResourceDetail):
    events = ArticleDetailEvent
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }
