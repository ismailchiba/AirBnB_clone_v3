#!/usr/bin/python3
""" app variable object of flask"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from flask_cors import CORS
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown(err):
    """ method to handle """
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """ handle for 404 errors """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
