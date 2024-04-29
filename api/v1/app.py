#!/usr/bin/python3
"""Status of your API"""

from flask import Flask, render_template, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def app_tear(error):
    """ calls methods close() """
    storage.close()


@app.errorhandler(404)
def handle_404_error(error):
    """ Loads a custom 404 page not found """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
