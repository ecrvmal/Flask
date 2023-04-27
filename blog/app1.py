from datetime import datetime

from flask import Flask, g
from flask import request

app = Flask(__name__)

visits = 0
routes = {}


@app.route('/<string:search>', methods=['GET'],)
def index(search: str):
    route_name = request.args.get('search', "")
    global routes
    if route_name in routes.keys():
        routes[route_name] += 1
    else:
        routes[route_name] = 1
    return f'You are {routes[route_name]} visitor of site 127.0.0.1:5000/{route_name}', 200


@app.route('/', methods=['GET'],)
def index():
    global visits
    visits += 1
    return f'You are {visits} visitor of site 127.0.0.1:5000/', 200

#
# @app.before_request
# def process_before_request():
#     """
#     Sets start_time to a object
#     """
#     g.start_time = datetime.now()
#
# @app.after_request
# def process_after_request(response):
#     """
#     adds process time in headers
#     """
#     if hasattr(g, "start_time"):
#         response.headers["process-time"] = datetime.now() - g.start_time
#     return response
#
#
# @app.errorhandler(404)                 # argument (404) or
# def handler_404(error):                # exception (timeOutError) (ConnectionError)
#     app.logger.error(error)            # in console - will be message
#     return "my_text_on_404"            # in browser text or return template here
#

# CALCULATOR APP
# @app.route('/<int:x>/<int:y>', methods=['DET', 'POST'])
# def index(x:int, y:int):
#     return f'Hello, {x ** y}'
