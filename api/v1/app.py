#!/usr/bin/python3
""" app """
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register the plueprint
app.register_blueprint(app_views)

CORS(app, resources={"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(error):
    """handle @app.teardown_appcontext that calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error handler"""
    """ handler for 404 error return in json format """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
