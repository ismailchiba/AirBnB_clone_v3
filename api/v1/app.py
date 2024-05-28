#!/usr/bin/python3
""" Create Flask Application
and register the blueprint app viewsto flask instance app. """

from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_engine(exception):
    """ Close Storage. """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """  404 Error. """
    responce = {"error": "Not found"}
    return jsonify(responce), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(debug=True, host=host, port=port, threaded=True)
