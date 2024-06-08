#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)

app.register_blueprint(app_views)



if __name__ == "__main__":
    """ Main Function """
    HOST = environ('HBNB_API_HOST', '0.0.0.0')
    PORT = int(environ('HBNB_API_PORT', 5000))
   
    app.run(host=HOST, port=PORT, threaded=True)
