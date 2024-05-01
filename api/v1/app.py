#!/usr/bin/python3
"""main app file."""
from flask import Flask, Blueprint
from os import getenv

app = Flask(__name__)
from models import storage
from api.v1.views import app_views
app.register_blueprint(app_views) # , url_prefix="/api/v1")

host = getenv('HBNB_API_HOST', default='0.0.0.0')
port = getenv('HBNB_API_PORT', default=5000)

@app.teardown_appcontext
def teardown(response_or_exc):
    """handle @app.teardown_appcontext that calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port, threaded=True)
