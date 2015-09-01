from flask import jsonify, request 
from wingo.api_v1 import api 
from wingo.models import Note
from wingo.utils import toJson, selectNotes

@api.route("/notes/<id>", methods=['GET'])
def get_note(id):
	try:
		note = Note.objects.get(id = id);
	except :
		raise ValidationError("not valid id")

	return toJson(note.export_data())


@api.route("/notes", methods=['GET'])
def get_notes_list(args):


	try:
		radius = args.get("radius")
	except:
		raise ValidationError("hahah")
	# lat  = args.get("lat")
	# lon  = args.get("lon")
	# search    = args.get("search",None)
	# nfilter = args.get("filter", "all")


	lat = 48.37073444524586
	lon = -4.479504229956185

	notes = selectNotes((lat,lon), radius)

	items = [n.export_data() for n in notes]
	return toJson(items)


@api.route("/notes", methods=['POST'])
def create_note():

	note = Note();
	note.import_data(request.json)
	note.save()

	return toJson({"id": str(note.id)})