from flask import jsonify, request , current_app
from wingo.api_v1 import api 
from wingo.models import Note
from wingo.utils import toJson, selectNotes
from wingo.auth import check_auth, current_user
from wingo.exceptions import CustomError
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs


#=================================================================

@api.route("/notes/<id>", methods=['GET'])
def get_note(id):
	""" 
	Get a note from ID 
	---
	tags:
		- notes 
	parameters:
		- name: id 
		  in: path 
		  description: Note id 
		  required: true 
		  type: string 
	"""
	try:
		note = Note.objects.get(id = id);
	except :
		raise ValidationError("not valid id")

	return toJson(note.export_data())

''' Get note list using lat, lon, sort , radius, filter and search arguments ''' 

#=================================================================

@api.route("/notes", methods=['GET'])
@use_kwargs({
	'lat'    : Arg(float, required=True),
	'lon'    : Arg(float, required=True),
	'sort'   : Arg(str,   required=False, default = "recent",
						  validate=lambda w: w in ["recent", "distance","popular"],
						  error   = "sort can be recent, distance or popular"),

	'radius' : Arg(str,   required = True,
						  validate=lambda w: w in ["small", "medium","large"] , 
						  error="radius should be small, medium or large"),

	'filter' : Arg(str,   required = False, default=None,
						  validate=lambda w: w in ["has_max_takes", "has_expiration"],
						  error   = "filter can be has_max_takes or has_expiration"),

	'search' : Arg(str, required=False, default=None)
	})

def get_notes_list(lat,lon,sort,radius,filter,search):
	""" 
	Get a note list
	---
	tags:
		- notes 
	parameters:
		- name: lat 
		  in: query 
		  required: true 
		  type: string
		  description: latitude
		  default: 48.4000000
		- name: lon 
		  in: query 
		  required: true 
		  type: string
		  description: longitude
		  default: -4.4833300
		- name: radius 
		  in: query 
		  type: string
		  required: true
		  description: (small or medium or large) 	
		  default: small
		- name: sort 
		  in: query 
		  type: string
		  description: (recent or distance or popular)		  
		- name: filter 
		  in: query 
		  type: string
		  description: (has_max_takes or has_expiration)	
		- name: search 
		  in: query 
		  type: string
		  description: tag keyword				  	
	"""

	if radius == "small":
		radius = current_app.config["SMALL_RADIUS"]

	if radius == "medium":
		radius = current_app.config["MEDIUM_RADIUS"]
	
	if radius == "large":
		radius = current_app.config["LARGE_RADIUS"]
	

	query  = selectNotes(center=(lat,lon), radius = radius, search = search)

	if sort == "recent": 
		query = query.order_by("timestamp")

	if sort == "distance":
		query = query;

	if sort == "popular":
		query = query.order_by("-takes")


	if filter is not None :
		if filter == "has_max_takes":
			query = query.filter(takes_limit__ne = None)

		if filter == "has_expiration":
			query = query.filter(expiration__ne = None)


	items = [n.export_data() for n in query]
	return toJson(items)

#=================================================================

@api.route("/notes", methods=['POST'])
@check_auth
@use_args({
	'lat'       : Arg(float, required=True),
	'lon'       : Arg(float, required=True),
	'message'   : Arg(str,   required=True),
	'media'     : Arg(str, required = False, default=None)
	})

def create_note(args):
	""" 
	Create a new note 
	---
	tags:
		- notes 
	parameters:
		- in: body 
		  name: body 
		  schema:
		  	id: Note 
		  	required:
		  		- lat
		  		- lon
		  		- message 
		  	properties:
		  		lat:
		  			type: string
		  			description: latitude
		  			default: 48.4000000
		  		lon: 
		  			type: string
		  			description: longitude 
		  			default: -4.4833300

				message:
					type: string 
					description: message
					default: This is a message
				media:
					type: string
					description: media url 
	"""

	print(args)
	note = Note();
	
	note.import_data(args)
	note.author = current_user()  

	note.save()

	return toJson({"id": str(note.id)})

#=================================================================

@api.route("/notes/take/<id>", methods=['POST'])
@check_auth
def take_note(id):
	""" 
	Take a note 
	---
	tags:
		- notes 
	parameters:
		- name: id 
		  in: path
		  description: Note id 
		  required: true
		  type: string
	"""
	note = Note.objects.get(pk= id);
	user = current_user()

	user.pocket_notes.append(note)
	note.takes+= 1 
	note.save()
	user.save()

	return toJson({"id": str(note.id)+ " has been taken"})
#=================================================================

@api.route("/notes/untake/<id>", methods=['POST'])
@check_auth
def untake_note(id):
	""" 
	Untake a note 
	---
	tags:
		- notes 
	parameters:
		- name: id 
		  in: path
		  description: Note id 
		  required: true
		  type: string
	"""
	note = Note.objects.get(pk= id);
	user = current_user()

	if note in user.pocket_notes:
		user.pocket_notes.remove(note)
		note.takes-=1
		note.save()
		user.save()
		return toJson({"id": str(note.id)+ " has been untaken"})
	else:
		raise CustomError("This note has not been taken by " + user.name)
#=================================================================

@api.route("/notes/<id>", methods=['DELETE'])
def del_note(id):
	""" 
	Delete a note from ID 
	---
	tags:
		- notes 
	parameters:
		- name: id 
		  in: path 
		  description: Note id 
		  required: true 
		  type: string 
	"""
	try:
		note = Note.objects.get(id = id);
	except :
		raise ValidationError("not valid id")

	# Do note remove it ! Make it disable 
	# note.delete()
	note.disabled = True 
	note.save()

	return toJson({"message": "Not has been disabled"})
