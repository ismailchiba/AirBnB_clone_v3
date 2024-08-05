#!/usr/bin/python3
""" Flask Application """
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Config Flask Application: app
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['DEBUG'] = True

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r'/*': {'origins': host}})


@app.teardown_appcontext
def close_db(error):
    """close storage"""
    storage.close()


@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """ Main Function """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port, threaded=True)
