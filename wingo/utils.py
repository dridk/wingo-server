from flask import jsonify
from wingo.models import Note

def toJson(data):
	if isinstance(data, dict):
		return jsonify({"success":True, "results": data})

	if isinstance(data, list):
		return jsonify({"success":True, "results":data, "total":len(data)})

	return jsonify({'status': 500, 'error': 'internal server error',"success": False,
                        'message': 'Bad python object parsing'})




def getNotes(center, radius = 10000 , keyword = None):

	if keyword is None: 
		queryset = 	Note.objects(location__near=center , location__max_distance=radius)
	else:
		queryset =  Note.objects(location__near=center , location__max_distance=radius, tags__contains=keyword)


	return queryset
