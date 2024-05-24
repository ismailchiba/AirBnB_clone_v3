#!/usr/bin/python3
"""
App.py, the central application for web app
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearContext(exception):
    """Function to tear the current context of
    the Flask app
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    custom error handler
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
