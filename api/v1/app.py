#!/usr/bin/python3
""" let's configure a flask app
"""


from flask import Flask
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_store(self):
    '''close the storage'''
    storage.close()

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
"""
def get_environment_variable(var_name, default_value):
    
    Retrieves the value of an environment variable
    or returns a default value if the variable is not set.
    
    return os.getenv(var_name, default_value)


if __name__ == "__main__":
    host = get_environment_variable('HBNB_API_HOST', '0.0.0.0')
    port = get_environment_variable('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
"""
