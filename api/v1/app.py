#!/usr/bin/python3
"""Module to create a flask app"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
import os

# create a variable app, instance of Flask
app = Flask(__name__)

# Creating a flask CORS
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


# handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """Method to handle teardown of app context"""
    storage.close()


# create a handler for 404 errors that returns a JSON-formatted 404 status
@app.errorhandler(404)
def nop(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Run the app
if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))

    # Start the Flask server
    app.run(host=host, port=port, threaded=True)
