#!/usr/bin/python3
""""""
from models import storage
from api.v1.views import app_views
from flask import Flask
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def cleanup(exc=None):
    """cleanup after each request"""
    storage.close()
    if exc:
        pass


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(debug=True, port=port, host=host)
