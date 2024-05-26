#!/bin/python3
# Status of your API

from flask import Flask
import storage from models
import app_views from api.v1.views

# Create an instance of the Flask class
app = Flask(__name__)

# Register the Blueprint with the Flask app
app.register_blueprint(app_views)

# Define a teardown method to close the storage
@app.teardown_appcontext
def close_storage(exception):
    """Teardown method to close the storage."""
    storage.close()
