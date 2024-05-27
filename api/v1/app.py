#!/usr/bin/env python3
"""
this modules starts a flask instanc
"""

from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)

port_no = int(getenv('HBNB_API_PORT', '5000'))
host_no = getenv('HBNB_API_HOST', '0.0.0.0')
app.register_blueprint(app_views)
@app.teardown_appcontext
def handle_teardown(exeption):
    storage.close()


if __name__ == "__main__":
    app.run(debug=True, host=host_no, port=port_no, threaded=True)
