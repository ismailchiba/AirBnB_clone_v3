#!/usr/bin/python3

"""
Flask web application api
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Return an 'error: not found' JSON response """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    my_host = os.getenv('HBNB_API_HOST')
    my_port = os.getenv('HBNB_API_PORT')
    app.run(host=my_host, port=int(my_port), threaded=True)
