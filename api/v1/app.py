#!/usr/bin/python3
"""
Creating app using flask
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_component(exception=None):
    """closing storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error page 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
    app.run()
