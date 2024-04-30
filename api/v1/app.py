#!/usr/bin/python3
"""The flask web application"""
import os
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_flask(exc):
    """closing the sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    response = ({"error": "Not found"})
    return jsonify(response), 404


if __name__ == "__main__":
    app_host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    app_port = os.environ.get('HBNB_API_PORT', '5000')
    app.run(host=app_host,
            port=app_port,
            threaded=True
            )
