#!/usr/bin/python3
"""Creates web application"""

from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


host = getenv('HBNB_API_HOST')
port = getenv('HBNB_API_PORT')

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port, threaded=True)
