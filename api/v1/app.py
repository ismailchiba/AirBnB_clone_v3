#!/usr/bin/python3
""" creating  a flask application """


from flask import Flask
import os
from models import storage
from api.v1.views import app_views

# create flask structure
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


# Define the method to handle teardown
@app.teardown_appcontext
def teardown_db(exxception):
    """ calls storage.close() on eardown """
    storage.close()


# Main entry point
if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
