#!/usr/bin/python3
"""create a variable app, instance of Flask"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """Close the storage."""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """handles 404 error"""
    return make_response(
        jsonify({'error': 'Not found'}), 404
    )


if __name__ == "__main__":
    """run your Flask server"""
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT') if getenv(
        'HBNB_API_PORT'
    ) is not None else 5000
    app.run(host=host, port=int(port), threaded=True)
