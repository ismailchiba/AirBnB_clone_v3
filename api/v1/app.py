#!/usr/bin/python3
"""
    Flask Application more comments more comments.
    It takes care of some routes.
    more comments commetns testting ccommnets
    more commentss cccccccccccccccccccc
    comments
"""

from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """
        Close will take care of cleanup for the class
        more comments here later
        comments comennts comments
        cmments cccccccccccccccccccccccccc
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """
        Main Function to start the main code
        more comments more comments
        comments comments comments
    """

    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
