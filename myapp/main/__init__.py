from flask import Blueprint

main = Blueprint('main', __name__)


from . import views, errors
from ..models import Permission

#define variable in all template
@main.app_context_processor
def injuect_permissions():
	return dict(Permission=Permission)
