from flask import jsonify
from wingo.models import Note

def toJson(data):

	if isinstance(data, list):
		return jsonify({"success":True, "results":data, "total":len(data)})

	else:
		return jsonify({"success":True, "results": data})







def selectNotes(center, radius = 10000 , search = None):

	if search is None: 
		queryset = 	Note.objects(location__near=center , location__max_distance=radius)
	else:
		queryset =  Note.objects(location__near=center , location__max_distance=radius, tags__contains=search)


	return queryset



