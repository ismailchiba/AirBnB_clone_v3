#!/usr/bin/python3
"""
App.py, the central application for web app
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def tearContext(exception):
    """Function to tear the current context of
    the Flask app
    """
    storage.close()

<<<<<<< HEAD
=======

>>>>>>> 9318b187df510795d09b3d8b5f024c72ff651049
@app.errorhandler(404)
def not_found(error):
    """
    custom error handler
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True)
