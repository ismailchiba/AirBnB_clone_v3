#!/usr/bin/python3
<<<<<<< HEAD
'''Contains a Flask web application API.

   Handles API requests and responses, error handling, and application context
   management.
'''
import os
from flask import Flask, jsonify
from flask_cors import CORS

=======
"""Start your API."""
import os
from flask import Flask, jsonify
from flask_cors import CORS
>>>>>>> cdb70463e75f202994319b40315a096d05ae4045
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
<<<<<<< HEAD
'''Configures the Flask application.'''
=======

>>>>>>> cdb70463e75f202994319b40315a096d05ae4045
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
<<<<<<< HEAD
    '''Closes the storage engine connection upon request/app context
    teardown.'''
=======
    """The Flask app request context end event listener."""
>>>>>>> cdb70463e75f202994319b40315a096d05ae4045
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
<<<<<<< HEAD
    '''Handles 400 Bad Request errors.

    Returns: JSON response with a more informative error message and status
    code 400.
    '''
=======
    """Handles 404 HTTP error code."""
>>>>>>> cdb70463e75f202994319b40315a096d05ae4045
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
<<<<<<< HEAD
    '''Handles 400 Bad Request errors.

    Returns: JSON response with a more informative error message and status
    code 400.
    '''
=======
    """Handles the 400 HTTP error code."""
>>>>>>> cdb70463e75f202994319b40315a096d05ae4045
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
