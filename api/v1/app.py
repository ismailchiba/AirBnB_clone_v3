#!/usr/bin/python3
"""create variable"""
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(obj):
    """registers a function when app contect is torn down"""
    storage.close()

@app.errorhandler(404)
def not_found_page(error):
    """return custom json fomatted 404 page not found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host, int(port), threaded=True)
