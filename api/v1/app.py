#!/usr/bin/python3
"""
    Api module
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
"""Flask instance"""
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
app_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
app_port = int(os.getenv("HBNB_API_PORT", "5000"))


@app.teardown_appcontext
def end_session(exception):
    """end session of a conn"""
    storage.close()


if __name__ == '__main__':
    app_host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    app_port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(
            host=app_host,
            port=app_port,
            threaded=True
           )
