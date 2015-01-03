import json
from flask import session
from wingo.models import Note, User



def SuccessResponse(data = None, **args):
	if data is None:
		results = {"success":True}
	else:
		if isinstance(data, list):
			results = {"success":True, "results":data, "total":len(data)}
		else:
			results = {"success":True, "results":data}

	for key in args:
		results[key] = args[key]

	return results



def ErrorResponse(message="Unknown", code="111"):
	results = {"success":False, "message":message, "error_code":code}
	return results



def tagsFromText(text):
	return [i for i in a.split(" ") if i.startswith("#")]



def check_auth(f):
	def called(*args, **kargs):
		if 'user_id' in session:
			user = User.from_id(session["user_id"])
			if user is not None:
				return f(*args, **kargs)
		return ErrorResponse("authentification is required")
	return called


def current_user():
	if 'user_id' in session:
		user = User.from_id(session["user_id"])
		return user