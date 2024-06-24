#!/usr/bin/python3
"""Status of your API"""

from flask import Flask, render_template, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def app_tear(error):
     """ calls methods close() """
     storage.close()

@app.errorhandler(404)
def handle_404_error(error):
    """ Loads a custom 404 page not found """
    error_response = {"error": "Not found"}
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
