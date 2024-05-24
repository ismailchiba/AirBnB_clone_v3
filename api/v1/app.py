#!/usr/bin/python3
"""
App.py, the central application for web app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def tearContext(exception):
    """Function to tear the current context of
    the Flask app
    """
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000', threaded=True)
