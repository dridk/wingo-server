from flask import jsonify, request , current_app
from wingo.api_v1 import api 
from wingo.models import Note
from wingo.utils import toJson, selectNotes
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs
@api.route("/notes/<id>", methods=['GET'])
def get_note(id):
	try:
		note = Note.objects.get(id = id);
	except :
		raise ValidationError("not valid id")

	return toJson(note.export_data())


@api.route("/notes", methods=['GET'])
@use_kwargs({
	'lat'    : Arg(float, required=True),
	'lon'    : Arg(float, required=True),
	'sort'   : Arg(str,   required=False, default = "recent",
						  validate=lambda w: w in ["recent", "distance","popular"]),

	'radius' : Arg(str,   required = True,
						  validate=lambda w: w in ["small", "medium","large"] , 
						  error="radius should be small, medium or large"),
	'filter' : Arg(str,   required = False, default=None,
						  validate=lambda w: w in ["has_max_takes", "has_expiration"]),
	'search' : Arg(float, required=False, default=None)
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


@api.route("/notes", methods=['POST'])
def create_note():

	note = Note();
	note.import_data(request.json)
	note.save()

	return toJson({"id": str(note.id)})