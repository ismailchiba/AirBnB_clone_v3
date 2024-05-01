#!/usr/bin/python3
"""create Flask app: and register the blueprint app_view to flask instance app.
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from models import amenity

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_engine(exception):
    '''
    
    '''
    storage.close()

    @app.errorhandler(404)
    def not_found(error):
      '''
    
      '''
      response = {"errir": "not_found"}
      return jsonify(response), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_POR", "5000"))
    app.run(debug = True,host=HOST, port=PORT, threaded=True)

