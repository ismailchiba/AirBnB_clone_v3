#!/usr/bin/python3
"""create a variable app, instance of Flask"""


from flask import Flask, jsonify, make_response, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_end(self):
    """declare a method to handle"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handles 404 error"""
    return make_response(
        jsonify({'error': 'Not found'}), 404
    )


if __name__ == "__main__":
    """run your Flask server"""
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default='5000'))
    app.run(host=host, port=port, threaded=True)
