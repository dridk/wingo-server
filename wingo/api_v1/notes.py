from flask import jsonify, request 
from wingo.api_v1 import api 
from wingo.models import Note
from wingo.utils import toJson


@api.route("/notes/<id>/", methods=['GET'])
def get_note(id):
	try:
		note = Note.objects.get(id = id);
	except :
		raise ValidationError("not valid id")

	return toJson(note.export_data())


@api.route("/notes/", methods=['GET'])
def get_notes_list():
	items = [n.export_data() for n in Note.objects.all()]
	return toJson(items[0:10])


@api.route("/notes/", methods=['POST'])
def create_note():

	note = Note();
	note.import_data(request.json)
	note.save()

	return toJson({"id": str(note.id)})