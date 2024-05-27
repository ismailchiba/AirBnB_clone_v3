#!/usr/bin/python3
"""
AirBnB clone - RESTful API using flask
"""
from os import getenv
from flask import Flask, render_template, request, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def do_teardown_appcontext(exception):
    """teardown method"""
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """handle 404 errors with a JSON response."""
    return jsonify({"error": "Not found"})


print(app.url_map)

if __name__ == "__main__":
    """run flask server"""
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
