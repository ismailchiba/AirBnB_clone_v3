#!/usr/bin/python3
from flask import Flask, Response, jsonify
from models import storage
from api.v1.views import app_views
import os
import json

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    """tear down app session"""

    storage.close()

@app.errorhandler(404)
def error_404(error):
    """ error handler 404 error """
    err = json.dumps({"error": "Not found"}, indent=2) + '\n'
    return err, 404

@app.errorhandler(400)
def error_400(error):
    """ error handler 400 error """

    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
   host = os.getenv("HBNB_API_HOST", "0.0.0.0")
   port = int(os.getenv("HBNB_API_PORT", 5000))
   app.run(host=host, port=port, threaded=True)
