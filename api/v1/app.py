#!/usr/bin/python3

import os
from models import storage
from flask import Flask, Blueprint
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)

@app.route('/api/v1/nop', methods=['GET'], strict_slashes=False)
def nope():
    """ Returns a 404 """
    return {"error": "Not found"}

@app.route('/status2', methods=['GET'], strict_slashes=False)
def status():
    """ Returns a JSON """
    return {"status": "OKAY"}

@app.teardown_appcontext
def close_session(exception):
    storage.close()


if __name__ == "__main__":
    # port = environment variable HBNB_API_PORT or 5000 if not defined
    # host = environment variable HBNB_API_HOST
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True, use_reloader=False)
