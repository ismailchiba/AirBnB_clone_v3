#!/usr/bin/python3
"""
create a api
"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardodwn_db(exception):
    """teardown"""
    storage.close()

if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
