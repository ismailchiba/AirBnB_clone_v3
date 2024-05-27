#!/usr/bin/python3
"""Creates a Flask web application"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """Handles 404 errors, returns JSON-formatted stat code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


# @app.errorhandler(400)
# def handle_bad_request(error):
#     """Custom error handler for 400 errors"""
#     response = error.get_response()
#     response.data = jsonify({
#         "code": error.code,
#         "name": "Bad Request",
#         "description": error.description
#     }).data
#     response.content_type = "application/json"
#     return response


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
