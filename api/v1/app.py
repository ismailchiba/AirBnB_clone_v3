#!/usr/bin/python3
""" airbnb api wih flask"""


from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearodwn_close(exception):
    """close data base"""
    storage.close()


@app.errorhandler(400)
def handle_request_error(exception):
    """Handle the request errors"""
    code = str(exception).split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(404)
def handle_request_error(exception):
    """Handle the request errors"""
    message = {'error': "Not found"}
    return make_response(jsonify(message), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
