from flask import Flask, Blueprint,jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    error_message = {
        'error': 'Not found'
    }
    return jsonify( error_message), 404

if__name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True, debug=True)

