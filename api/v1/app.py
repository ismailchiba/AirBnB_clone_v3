#!/usr/bin/python3
from flask import Flask
from models import storage
import os
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

host = os.environ.get('HBNB_API_HOST')
port = os.environ.get('HBNB_API_PORT')

@app.teardown_appcontext
def handle_teardown(evt):
    storage.close()

if __name__ == "__main__":
    app.run(
        host=f"{host or '0.0.0.0'}",
        port=f"{port or '5000'}",
        threaded=True
    )
