#!/usr/bin/python3
""" this is my API """
from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views
from os import environ
from werkzeug.exceptions import BadRequest
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    not_found = {'error': 'Not found'}
    return jsonify(not_found), 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    if environ['HBNB_API_HOST']:
        HOST = environ['HBNB_API_HOST']
    else:
        HOST = '0.0.0.0'
    if environ['HBNB_API_PORT']:
        PORT = environ['HBNB_API_PORT']
    else:
        PORT = '5000'

    app.run(host=HOST, port=PORT, threaded=True, debug=True)
