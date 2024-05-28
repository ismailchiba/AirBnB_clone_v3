#!/usr/bin/python3
'''
    to start creating api will initiate wih creating endpoints
'''
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', '5000'))
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_app(code):
    '''
        Handles teardown
    '''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''
        Returns a JSON-formatted error response
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
