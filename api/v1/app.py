#!/usr/bin/python3
"""Endpoint route will be to return the status of your API
"""


from flask import Flask
from api.v1.views import app_views
import os
from flask import jsonify
from models import storage
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handling the 404 json
    Not Found errors
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """Run the Flask application"""
    host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    port = os.getenv('HBNB_API_PORT', default='5000')
    app.run(host=host, port=port, threaded=True)
