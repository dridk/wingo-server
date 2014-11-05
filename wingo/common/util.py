import json



def SuccessResponse(data = None):
	if data is None:
		results = {"success":True}
	else:
		if isinstance(data, list):
			results = {"success":True, "results":data, "total":len(data)}
		else:
			results = {"success":True, "results":data}
	return results



def ErrorResponse(message="Unknown", code="111"):
	results = {"success":False, "message":message, "error_code":code}
	return results



def tagsFromText(text):
	return [i for i in a.split(" ") if i.startswith("#")]
