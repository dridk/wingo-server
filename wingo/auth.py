from wingo.models import User
from wingo.exceptions import CustomError
from flask import session

''' Authentification decorator using session ''' 
def check_auth(f):
	def called(*args, **kargs):
		print("session")
		if 'user_id' in session:
			user = User.from_id(session["user_id"])
			if user is not None:
				return f(*args, **kargs)
		else:	
			print("n'est pas la ")
			raise CustomError("authentification is required")
	return called


''' Return current user from session ''' 
def current_user():
	if 'user_id' in session:
		user = User.from_id(session["user_id"])
		return user
	return None