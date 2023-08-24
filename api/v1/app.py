#!/usr/bin/python3
"""Import Modules"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv

"""Start Flask"""
app = Flask(__name__)

"""Register the blueprint app_views"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(Exception):
    """Close session"""
    storage.close()

@app.errorhandler(404)
def errorhandler(error):
    """Returns a JSON-formated status code for errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
