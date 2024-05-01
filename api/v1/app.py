#!/usr/bin/python3
""" A module that contains the flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exc):
    """ closes the session """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    """ Handling the page not found """
    return jsonify({"error":"Not found"})



if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(debug=True, host=host, port=port, threaded=True)
