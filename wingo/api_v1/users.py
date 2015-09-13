from flask import jsonify, request , session, current_app
from wingo.api_v1 import api 
from wingo.models import User, Note
from wingo.exceptions import CustomError
from wingo.utils import toJson
from wingo.auth import check_auth, current_user
from webargs.flaskparser import use_args, use_kwargs
from webargs import Arg

#=====================================================
@api.route("/users/<string:id>", methods=['GET'])
def get_user(id):
	""" 
	Get a user from Id 
	---
	tags:
		- users 
	parameters:
	 - name: id 
	   in: path
	   required: true
	   type: string
	   description: User id 

	"""
	try:
		user = User.objects.get(id = id);
	except :
		raise CustomError("not a valid id")

	return toJson(user.export_data())

#=====================================================

@api.route("/users", methods=['GET'])
@check_auth
def get_users_list():
	""" 
	Get a user list 
	---
	tags:
		- users 
	"""
	users = User.objects.all()
	results = [u.export_data() for u in users]
	return toJson(results)

#=====================================================

@api.route("/users", methods=['POST'])
@use_args({
	'name'    : Arg(str, required=True),
	'email'   : Arg(str, required=True),
	'password': Arg(str, required=True),
	'avatar'  : Arg(str, required=False, default=None)
	})
def create_user(args):
	""" 
	Create a new user 
	---
	tags:
		- users 
	parameters:
		- in: body 
		  name: body 
		  schema:
		  	id: User 
		  	required:
		  		- name
		  		- email
		  		- password 
		  	properties:
		  		name:
		  			type: string
		  			description: User name  
		  		email: 
		  			type: string
		  			description: email 
				password:
					type: string 
					description: string
				avatar:
					type: string
					description: avatar
	"""
	user = User();
	user.import_data(args)
	user.save()
	return toJson({"id": str(user.id)})

#=====================================================

@api.route("/users/<id>/notes", methods=['GET'])
def get_user_notes(id):
	""" 
	Get all published note for the user 
	---
	tags:
		- notes 
	parameters:
		- name: id 
		  in: path 
		  description: User id 
		  required: true 
		  type: string 
	"""
	user = User.objects.get(id = id)
	items = [i.export_data() for i in user.notes]
	return toJson(items)

#=====================================================

@api.route("/users/<id>/pocket", methods=['GET'])
def get_user_pocket(id):
	""" 
	Get all pocket note for the user 
	---
	tags:
		- notes 
	parameters:
		- name: id 
		  in: path 
		  description: User id 
		  required: true 
		  type: string 
	"""
	user = User.objects.get(id = id)
	items = [i.export_data() for i in user.pocket_notes]
	return toJson(items)

#=====================================================

@api.route("/users/login", methods=['POST'])
@use_kwargs({
	'email'   : Arg(str, required = True),
	'password': Arg(str, required = True)
	})
def login(email, password):
	""" 
	Login 
	---
	tags:
		- users 
	parameters:
		- in: body 
		  name: body 
		  schema:
		  	id: Login
		 	required:
		  	  - email
		  	  - password 
		  	properties:
		  		email:
		  			type: string
		  			description: email 
		  		password:
		  			type: string
		  			description: password


	"""
	try:
		user = User.objects.get(email=email, password=password)
	except :
		raise CustomError("Wrong email or password")
		session.pop("user_id", None)

	else:
		session["user_id"] = str(user.id)
	return toJson({"message": "logged"})

#=====================================================

@api.route("/users/logout", methods=['DELETE'])
def logout():
	""" 
	Logout
	---
	tags:
		- users 
	"""
	session.pop("user_id")
	return toJson({"message": "logout"})

#=====================================================

@api.route("/users/me", methods=['GET'])
@check_auth
def get_me():
	""" 
	Get current user  
	---
	tags:
		- users 
	"""
	user = current_user()
	return toJson(user.export_data())


#=====================================================

@api.route("/users/<id>", methods=['DELETE'])
@check_auth
def del_user(id):
	""" 
	delete user  
	---
	tags:
		- users
	parameters:
		- name: id 
		  in: path 
		  description: User id
		  required: true
		  type: string
	"""
	try:
		user = User.objects.get(id = id);
	except :
		raise CustomError("not a valid id")

	user.delete()

	return toJson({"message" : "user deleted"})


