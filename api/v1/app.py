#!/usr/bin/python3
"""app instance of flask"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """teardown function"""
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """handles 404 error"""
    data = {
        "error": "Not found"
    }
    resp = make_response(jsonify(data), 404)
    return(resp)

if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
