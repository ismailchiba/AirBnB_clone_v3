from flask import Flask
from models import storage
from api.v1.views import app_views
import os

# Create a Flask application instance
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Define a method to handle app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage when the app context is torn down"""
    storage.close()

if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))

    # Run the Flask server
    app.run(host=host, port=port, threaded=True)
