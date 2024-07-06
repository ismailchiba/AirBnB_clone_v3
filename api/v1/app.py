#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(close):
    storage.close()

@app.errorhandler(404)
def not_found_error(exception):
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
