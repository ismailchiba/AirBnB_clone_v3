#!/usr/bin/python3
"""
app
"""

from flask import Flask, jsonify
# from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


<<<<<<< HEAD
#creating an instance of flask
=======
>>>>>>> 8471f4eadde8806234297f3b75e7ad8d245a4f73
app = Flask(__name__)

# CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


<<<<<<< HEAD
if __name__ == "__main__":
    # Getting host and port from environment variables, or using default values
=======
@app.teardown_appcontext
def teardown(exception):
    """
    teardown function
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 error
    :return: returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return(resp)

if __name__ == "__main__":
>>>>>>> 8471f4eadde8806234297f3b75e7ad8d245a4f73
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
