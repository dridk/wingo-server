from flask import jsonify, request 
from wingo.api_v1 import api 
from wingo.models import User, Note
from wingo.exceptions import CustomError
from wingo.utils import toJson
from webargs.flaskparser import use_args
from webargs import Arg




@api.route("/users/<id>", methods=['GET'])
def get_user(id):
	try:
		user = User.objects.get(id = id);
	except :
		raise CustomError("not a valid id")

	return toJson(user.export_data())


@api.route("/users", methods=['GET'])
def get_users_list():
	users = User.objects.all()
	results = [u.export_data() for u in users]
	return toJson(results)


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



@api.route("/users/<id>/notes", methods=['GET'])
def get_user_notes(id):
	user = User.objects.get(id = id)
	items = [i.export_data() for i in user.notes]
	return toJson(items)



@api.route("/users/<id>/pocket", methods=['GET'])
def get_user_pocket(id):
	user = User.objects.get(id = id)
	items = [i.export_data() for i in user.pocket_notes]
	return toJson(items)





