#!/usr/bin/python3
""" A Flask API """
import flask from Flask
from models import storage
from api.v1.views import api_views

app = Flask(__name__)

""" Register blueprints """
app.register_blueprint(app_views)


""" Method to handle teardown_appcontext """
@app.teardown_appcontext(exception):
    storage.close() 



if __name__ == "__main__":
    host = os.env.get("HBNB_API_HOST", "0.0.0.0"
    port = int(os.env.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
