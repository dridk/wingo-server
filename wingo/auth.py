from wingo.models import User
from wingo.exceptions import CustomError
from flask import session
import functools

''' Authentification decorator using session ''' 
def check_auth(f):

	@functools.wraps(f)
	def wrapped(*args, **kargs):
		if 'user_id' in session:
			user = User.from_id(session["user_id"])
			if user is not None:
				return f(*args, **kargs)
		else:	
			raise CustomError("authentification required")

	return wrapped


''' Return current user from session ''' 
def current_user():
	if 'user_id' in session:
		user = User.from_id(session["user_id"])
		return user
	return None