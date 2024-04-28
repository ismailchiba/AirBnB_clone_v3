#!/usr/bin/python3
"""Flask server (variable app)
"""


from flask import Flask
from flask import jsonify
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.teardown_appcontext
def downtear(self):
    '''Status of your API'''
    storage.close()

@app.errorhandler(404)
def not_found(error):
    response jsonify ({'error': 'Not found'})
    response.status_code = 404
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
