#!/usr/bin/python3
"""
Module to create API with Flask
"""
from flask import Flask, jsonify
from models import storage
from models.engine import *
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


''' Flask Instance '''
app = Flask(__name__)

''' Register Blueprint '''
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(error):
    '''
    Remove the database, the save the file and exit
    '''
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''
    Error 404 handler
    '''
    return(jsonify(error="Not Found"), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
