#!/usr/bin/python3
"""This is our flask instance"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """teardown function"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """returns a 404 response and a json answer"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
