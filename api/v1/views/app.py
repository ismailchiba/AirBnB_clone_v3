#!/usr/bin/python3
"""It’s time to start your API!"""


from models import storage as s
from api.v1.views import app_views as av
from flask import Flask as f
import os


app = f(__name__)
app.register_blueprint(av)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """just call storage close"""
    s.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port= port, threaded=True)
