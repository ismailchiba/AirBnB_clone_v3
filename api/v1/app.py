#!/usr/bin/python3
"""
<<<<<<< HEAD
app"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    ''' closes storage engine '''
=======
API for AirBnB_clone_v3
"""

import os
from flask import Flask, jsonify, Response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """ handles teardown """
>>>>>>> 76e9b7a83b6178fbb7b20d3026cfb7422a70b8a3
    storage.close()


@app.errorhandler(404)
<<<<<<< HEAD
def not_found(error):
    ''' handles 404 error and gives json formatted response '''
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    if getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = '0.0.0.0'
    else:
        HBNB_API_HOST = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = 5000
    else:
        HBNB_API_PORT = int(getenv("HBNB_API_PORT"))
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
=======
def page_not_found(e):
    """ handles 404 errors """
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    try:
        host = os.environ.get('HBNB_API_HOST')
    except:
        host = '0.0.0.0'

    try:
        port = os.environ.get('HBNB_API_PORT')
    except:
        port = '5000'

    app.run(host=host, port=port)
>>>>>>> 76e9b7a83b6178fbb7b20d3026cfb7422a70b8a3
