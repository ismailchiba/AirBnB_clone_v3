#!/usr/bin/python3
""" endpoint (route) will be to return the status of your API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from werkzeug.exceptions import HTTPException
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage engine"""
    storage.close()

@app.errorhandler(404)
def not_found_error(error):
    """ Return a custom 404 error """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
