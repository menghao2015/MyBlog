from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .models  import Permission

def permission_required(permission):
	def decorators(f):
		@wraps(f)
		def decorators_function(*args, **kwargs):
			if not current_user.can(permission):
				abort(403)
			return f(*args, **kwargs)
		return decorators_function
	return decorators

def admin_required(f):
	return permission_required(Permission.ADMINISTER)(f)


	
