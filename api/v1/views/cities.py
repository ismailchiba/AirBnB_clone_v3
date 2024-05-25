from api.v1.views import city_views
from models import storage
from models.state import State

all_cities = storage.all(State)
# @city_views.route("/")
