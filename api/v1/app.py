#!/usr/bin/python3
"""
this modules starts a flask instance
"""
from flask import Flask, jsonify, make_response, Blueprint
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def error404(e):
    """ instance of app to handle 404 errors """
    response = {"error": "Not found"}
    return make_response(jsonify(response), 404)


port_no = int(getenv('HBNB_API_PORT', '5000'))
host_no = getenv('HBNB_API_HOST', '0.0.0.0')
app.register_blueprint(app_views)


@app.teardown_appcontext
def handle_teardown(exeption):
    """exit the api in case of unexpected error"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=host_no, port=port_no, threaded=True)
