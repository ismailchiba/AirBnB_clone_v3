#!/usr/bin/python3
"""
This module contains the principal application
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
#!/usr/bin/python3
"""
This module contains the principal application
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(obj):
    """ calls methods close() """
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """create a handler for 404 errors
       that returns a JSON-formatted
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    host = os.getenv('HBNB_API_HOST' '0.0.0.0')
    port = os.getenv('HBNB_API_PORT' '5000')

    app.run(host=host, port=port, threaded=True)
