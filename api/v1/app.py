#!/usr/bin/python3
"""
app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

 # Registering the app_views blueprint
 app.register_blueprint(app_views)

 # Method to handle app teardown
 @app.teardown_appcontext
 def teardown_db(exception):
         storage.close()

if __name__=="__main__":
    # Running the Flask server with specified host and port
        host = os.getenv('HBNB_API_HOST', '0.0.0.0')
            port = int(os.getenv('HBNB_API_PORT', 5000))
                app.run(host=host, port=port, threaded=True)

