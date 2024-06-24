#!/usr/bin/python3
"""
    Api module
"""
import os
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""Flask instance"""
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
app_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
app_port = int(os.getenv("HBNB_API_PORT", "5000"))
CORS(app, resources={"/*": {"origins": app_host}})


@app.teardown_appcontext
def end_session(exception):
    """end session of a conn"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """custom 404- not found error"""
    return make_response(jsonify(error="Not found"),
                         404)


if __name__ == '__main__':
    app_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    app_port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(
            host=app_host,
            port=app_port,
            threaded=True
           )
