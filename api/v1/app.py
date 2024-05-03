#!/usr/bin/python3

"""
Flask App for Airbnb (v3) project
"""
from flask import Flask, jsonify, render_template, make_response, url_for
from flask_cors import CORS, cross_origin
from api.v1.views import app_views
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Flask server
app = Flask(__name__)

app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """calls .close() on current SQLAlchemy Session."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def handle_400(exception):
    """Alternatively handles 400 errros."""
    err_code = exception.__str__().split()[0]
    desc = exception.description
    msg = {'error': desc}
    return make_response(jsonify(msg), err_code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """Global Route to handle All Error Status Codes."""
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
    """This updates HTTPException Class with custom error function."""
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    setup_global_errors()
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000),
            threaded=True)
