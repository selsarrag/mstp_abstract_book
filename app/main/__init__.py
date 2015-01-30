from flask import Blueprint
#from ..models import Permission 

main = Blueprint('main', __name__)


from . import views, errors
