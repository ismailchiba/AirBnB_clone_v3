#!/usr/bin/python3
"""Main module for the API."""
from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """close storage engine"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''return render_template'''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    # host = getenv('HBNB_API_HOST')
    # port = getenv('HBNB_API_PORT')
    app.run(host='0.0.0.0', port='5000', threaded=True)
