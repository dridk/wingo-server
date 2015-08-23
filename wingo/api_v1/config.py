from flask import jsonify, request , current_app
from wingo.api_v1 import api 
from wingo.models import User

@api.route("/config/", methods=['GET'])
def get_config():

	res = {
		"radius" : current_app.config.get("RADIUS"),
		"max_note_length" : current_app.config.get("MAX_NOTE_LENGTH"),
		"version_name" : current_app.config.get("VERSION_NAME"),
    	"version" : current_app.config.get("VERSION"),
    	"note_per_page" : current_app.config.get("NOTE_PER_PAGE"),
    	"debug" :current_app.config.get("DEBUG")
	}

	return jsonify(res)