#!/usr/bin/python3
"""
app
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

<<<<<<< HEAD
#creating an instance of flask
app = Flask(__name__)

app.register_blueprint(app_views)

if __name__ == "__main__":
    # Getting host and port from environment variables, or using default values
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
=======
#instance f flask
app = Flask(__name__)

 # Registering the app_views blueprint
 #done when you dont to create every function/methods for app
app.register_blueprint(app_views)

 # Method to handle app teardown
#@app.teardown_appcontext
#def teardown_db(exception):
 #        storage.close()

if __name__=="__main__":
    # Running the Flask server with specified host and port
        host = os.getenv('HBNB_API_HOST', '0.0.0.0')
        port = int(os.getenv('HBNB_API_PORT', 5000))
        app.run(host=host, port=port, threaded=True)

>>>>>>> storage_get_count
