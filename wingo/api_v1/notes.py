from flask import jsonify, request 
from wingo.api_v1 import api 
from wingo.models import Note

@api.route("/notes/", methods=['GET'])
def get_notes():

	all = [n.export_data() for n in Note.objects.all()]
	print(all)
	return jsonify({"results": all})