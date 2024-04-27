#!/usr/bin/python3
'''this module creates a flask app'''

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    '''closes storage'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''returns a 404 error'''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        hostname = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
