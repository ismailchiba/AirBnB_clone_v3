#!/usr/bin/python3
""" Starting Flask web Application """


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(self):
    """ Call storage.close """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ returns a JSON-formatted 404 status code response
    """
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
