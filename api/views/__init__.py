from flask import Blueprint
from api.v1.views.index import view_function1, view_function2, view_class1

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import specific functions or classes from the index module
from api.v1.views.index import view_function1, view_function2, view_class1
