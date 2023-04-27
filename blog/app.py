from datetime import datetime

from flask import Flask, g
from flask import request

app = Flask(__name__)

visits = 0
routes = {}


@app.route('/<string:r_name>', methods=['GET'],)
def custom_index(r_name: str):
    global routes
    if r_name in routes.keys():
        routes[r_name] += 1
    else:
        routes[r_name] = 1
    return f'You are {routes[r_name]} visitor of site 127.0.0.1:5000/{r_name}', 200


@app.route('/', methods=['GET'],)
def root_index():
    global visits
    visits += 1
    return f'You are {visits} visitor of site 127.0.0.1:5000/', 200

# app.add_url_rule('/<search>', view_func=custom_index, methods=['GET', 'POST'])
# app.add_url_rule('/', view_func=root_index)
