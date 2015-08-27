from flask import jsonify

def toJson(data):
	if isinstance(data, dict):
		return jsonify({"success":True, "results": data})

	if isinstance(data, list):
		return jsonify({"success":True, "results":data, "total":len(data)})

	return jsonify({'status': 500, 'error': 'internal server error',"success": False,
                        'message': 'Bad python object parsing'})

