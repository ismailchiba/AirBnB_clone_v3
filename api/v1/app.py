#!/usr/bin/python3
"""app file"""
from flask import Flask
import os
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

host = os.getenv("HBNB_API_HOST", "0.0.0.0")
port = os.getenv("HBNB_API_PORT", "5000")

@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
