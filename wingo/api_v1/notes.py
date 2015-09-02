from flask import jsonify, request , current_app
from wingo.api_v1 import api 
from wingo.models import Note
from wingo.utils import toJson, selectNotes
from wingo.auth import check_auth, current_user
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs

''' Get note by id ''' 

@api.route("/notes/<id>", methods=['GET'])
def get_note(id):
	try:
		note = Note.objects.get(id = id);
	except :
		raise ValidationError("not valid id")

	return toJson(note.export_data())

''' Get note list using lat, lon, sort , radius, filter and search arguments ''' 

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

	radius = current_app.config["RADIUS"][radius]
	query  = selectNotes(center=(lat,lon), radius = radius, search = search)

	if sort == "recent": 
		query = query.order_by("timestamp")

	if sort == "distance":
		query = query;

	if sort == "popular":
		query = query.order_by("takes")


	if filter is not None :
		if filter == "has_max_takes":
			query = query.filter(takes_limit__ne = None)

		if filter == "has_expiration":
			query = query.filter(expiration__ne = None)


	items = [n.export_data() for n in query]
	return toJson(items)


''' Create a new note ''' 

@api.route("/notes", methods=['POST'])
@check_auth
@use_args({
	'lat'       : Arg(float, required=True),
	'lon'       : Arg(float, required=True),
	'message'   : Arg(str,   required=True),
	'media'     : Arg(str, required = False, default=None)
	})

def create_note(args):

	print(args)
	note = Note();
	
	note.import_data(args)
	note.author = current_user()  

	note.save()

	return toJson({"id": str(note.id)})



''' Take a note for the current user ''' 

@api.route("/notes/take/<id>", methods=['POST'])
@check_auth
def take_note(id):

	note = Note.objects.get(pk= id);
	user = current_user()

	user.pocket_notes.append(note)
	note.takes+= 1 
	note.save()
	user.save()

	return toJson({"id": str(note.id)+ " has been taken"})