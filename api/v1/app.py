#!/usr/bin/python3

"""Run Flask app at port 5000"""


from api.v1.views import app_views as AV
from flask import Flask as F, make_response as MR, jsonify
from models import storage
from os import getenv
from werkzeug.exceptions import HTTPException


app = F(__name__)

app.url_map.strict_slashes = False

"""Flask sys env variables"""
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown_db(code):
    """ Close db storage - Task 3 """
    storage.close()


@app.errorhandler(Exception)
def handle_all_errors(error):
    """ Handle global errors using HTTPException- Task 5 """
    if isinstance(error, HTTPException):
        if type(error).__name__ == 'NotFound':
            error.description = "Not found"
        msg = {'error': error.description}
        code = error.code
    else:
        msg = {'error': error}
        code = 500
    return MR(jsonify(msg), code)


def init_errors():
    """ Initialise handling errors for all sub classes """
    for single in HTTPException.__subclasses__():
        app.register_error_handler(single, handle_all_errors)


app.register_blueprint(AV)


if __name__ == '__main__':
    app.run(host=str(host), port=int(port), threaded=True)
