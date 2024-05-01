from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing index.py here might cause a circular import issue,
# so import it within the route where it's needed.
from api.v1.views.index import *
