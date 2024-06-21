#!/usr/bin/python3

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views, app_states, app_cities, app_amenities
from api.v1.views import app_users, app_places, app_places_reviews

HBNB_API_HOST = '0.0.0.0'
HBNB_API_PORT = '5000'

app = Flask(__name__)
"""<----------------- view routes ----------------->"""
app.register_blueprint(app_views, url_prefix="/api/v1")

"""<---------------- states routes ---------------->"""
app.register_blueprint(app_states, url_prefix="/api/v1/states")

"""<---------------- cities routes ---------------->"""
app.register_blueprint(app_cities, url_prefix="/api/v1/states",
                       name="state->cities")
app.register_blueprint(app_cities, url_prefix="/api/v1/cities",
                       name="cities")

"""<--------------- amenities routes -------------->"""
app.register_blueprint(app_amenities, url_prefix="/api/v1/amenities")

"""<----------------- users routes ---------------->"""
app.register_blueprint(app_users, url_prefix="/api/v1/users")

"""<---------------- places routes ---------------->"""
app.register_blueprint(app_places, url_prefix="/api/v1/cities",
                       name="city->places")
app.register_blueprint(app_places, url_prefix="/api/v1/places",
                       name="places")

"""<---------------- reviews routes --------------->"""
app.register_blueprint(app_places_reviews, url_prefix="/api/v1/places",
                       name="place->reviews")
app.register_blueprint(app_places_reviews, url_prefix="/api/v1/reviews",
                       name="reviews")


@app.teardown_appcontext
def teardown_db(exception=None):
    """ This function called each time the database is updated
    """
    storage.close()


"""<---------------- error handling --------------->"""
@app.errorhandler(400)
def name_not_found(msg):
    """ This function handels status_code '400'
    """
    return jsonify({'error': msg.description}), 400


@app.errorhandler(404)
def not_found(error):
    """ This function handels status_code '404'
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST,
            port=HBNB_API_PORT,
            threaded=True,
            debug=True)
