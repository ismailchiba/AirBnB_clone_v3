from flask import Blueprint

#creating a variable appviews
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing views to avoid circular imports
from api.v1.views import index
