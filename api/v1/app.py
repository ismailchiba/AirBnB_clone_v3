#!/usr/bin/python3
"""
starts a Flask web application
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


def launch(host=None, port=None):
    """App Launcher"""
    # Set default values if none provided
    host = host or "0.0.0.0"
    port = port or "5000"
    app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    launch()
