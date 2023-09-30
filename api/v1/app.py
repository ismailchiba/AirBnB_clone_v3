#!/usr/bin/python3
""" 
    V1 App creation module
"""

from flask import Flask, request
from markupsafe import escape

import os
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

#  register a blueprint 'app_views'
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

@app.teardown_appcontext
def teardown_db(exception):
    """ 
        Close MySQL session
    """
    storage.close()


if __name__ == '__main__':
    """ 
        run main flask web app 
    """
    app.run(threaded=True, host=host, port=port)
