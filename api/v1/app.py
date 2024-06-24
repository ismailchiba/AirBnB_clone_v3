#!/usr/bin/python3
"""
Create Flask app, and register the blueprint for app_views
"""

from os import getenv
from flask import Flask, jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, origins=['0.0.0.0'])

app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """ 404 page not found """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def not_a_json(error):
    """400 error"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    elif not request.get_json().get('name', None):
        return jsonify({"error": "Missing name"}), 400


@app.teardown_appcontext
def teardown(e):
    """close any current active route"""
    storage.close()


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
