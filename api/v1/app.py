#!/usr/bin/python3
"""Flask application and register the blueprint app_views flask"""

from flask import Flask
from api.v1.views import app_views
from models import storage
from flask_cors import Cosrs


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

cors = Cors(app, resources={r"/*":{"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ return render_template"""
    return jsonfy({"error": "Not found"}), 404



if __name__ == "__main__":
    import os
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)

