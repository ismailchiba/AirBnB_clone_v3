from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

HBNB_API_HOST = getenv("HBNB_API_HOST")
HBNB_API_PORT = getenv("HBNB_API_PORT")

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(error):
    """Close the storage connection."""
    storage.close()

if __name__ == '__main__':
    app.run(host=HBNB_API_HOST or '0.0.0.0',
            port=HBNB_API_PORT or '5000',
            threaded=True)
