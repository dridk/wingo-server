from flask import jsonify, request , session, current_app
from wingo.api_v1 import api 
from wingo.models import User, Note
from wingo.exceptions import CustomError
from wingo.utils import toJson
from wingo.auth import check_auth, current_user
from webargs.flaskparser import use_args, use_kwargs
from webargs import Arg
from flask_swagger import swagger

''' Get user id ''' 
@api.route("/users/<id>", methods=['GET'])
def get_user(id):
	try:
		user = User.objects.get(id = id);
	except :
		raise CustomError("not a valid id")

	return toJson(user.export_data())

''' Get user list ''' 
@api.route("/users", methods=['GET'])
@check_auth
def get_users_list():
	users = User.objects.all()
	results = [u.export_data() for u in users]
	return toJson(results)


''' Create a new user ''' 
@api.route("/users", methods=['POST'])
@use_args({
	'name'    : Arg(str, required=True),
	'email'   : Arg(str, required=True),
	'password': Arg(str, required=True),
	'avatar'  : Arg(str, required=False, default=None)
	})
def create_user(args):
	user = User();
	user.import_data(args)
	user.save()

	return toJson({"id": str(user.id)})


''' Get all published note from a user ''' 
@api.route("/users/<id>/notes", methods=['GET'])
def get_user_notes(id):
	user = User.objects.get(id = id)
	items = [i.export_data() for i in user.notes]
	return toJson(items)


''' Get all pocket note from a user ''' 
@api.route("/users/<id>/pocket", methods=['GET'])
def get_user_pocket(id):
	user = User.objects.get(id = id)
	items = [i.export_data() for i in user.pocket_notes]
	return toJson(items)

''' Login a create a session token ''' 
@api.route("/users/login", methods=['POST'])
@use_kwargs({
	'email'   : Arg(str, required = True),
	'password': Arg(str, required = True)
	})
def login(email, password):
	"""
        login to the user 
        ---
        tags:
          - users

    """



 
	try:
		user = User.objects.get(email=email, password=password)
	except :
		raise CustomError("Wrong email or password")
		session.pop("user_id", None)

	else:
		session["user_id"] = str(user.id)
	return toJson({"message": "logged"})


''' Logout and destroy the session token ''' 
@api.route("/users/logout", methods=['DELETE'])
def logout():
	session.pop("user_id")
	return toJson({"message": "logout"})


''' Get current user information  ''' 
@api.route("/users/me", methods=['GET'])
@check_auth
def get_me():
	user = current_user()
	return toJson(user.export_data())



''' Get current user information  ''' 
@api.route("/spec", methods=['GET'])
def spec():
	swag = swagger(current_app)
	swag['info']['version'] = "1.0"
	swag['info']['title'] = "My API"
	return jsonify(swag)


