#!/usr/bin/python3
'''
app
'''
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

def handle_404(exception):
    # Handler for 404 errors
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response

if __name__ == "__main__":
    # Set the host and port
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    
    #run your Flask server
    app.run(host=HOST, port=PORT, threaded=True)
