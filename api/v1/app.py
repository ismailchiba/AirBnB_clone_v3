#!/usr/bin/python3
from os import getenv

from flask import Flask

from api.v1.views import app_views
from models import storage

API_HOST = getenv("HBNB_API_HOST") or "0.0.0.0"
API_PORT = getenv("HBNB_API_PORT") or 5000

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(self):
    storage.close()


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, threaded=True)
