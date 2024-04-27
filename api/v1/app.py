#!/usr/bin/python3
"""  endpoint (route) will be to return the status of the API """

from models import storage
from api.v1.views import app_views
from flask import Flask
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    app.config['SERVER_NAME'] = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app.config['SERVER_PORT'] = os.getenv('HBNB_API_PORT', '5000')
    app.run(threaded=True)
