#!/usr/bin/python3
"""The Developnment of a REST API"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
