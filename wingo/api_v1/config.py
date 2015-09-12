from flask import jsonify, request , current_app
from wingo.api_v1 import api 
from wingo.models import User

@api.route("/config/", methods=['GET'])
def get_config():
	""" 
	Get API information
	---
	tags:
		- config 
	"""
	res = { 
		"radius" 			: current_app.config.get("RADIUS"),
		"max_note_length" 	: current_app.config.get("MAX_NOTE_LENGTH"),
		"version_name" 		: current_app.config.get("VERSION_NAME"),
		"version" 			: current_app.config.get("VERSION"),
		"note_per_page" 	: current_app.config.get("NOTE_PER_PAGE"),
		"debug" 			: current_app.config.get("DEBUG"),
		"configuration"     : current_app.config.get("CONFIG_NAME"),
		"db_host" 	        : current_app.config.get("DB_HOST"),
		"db_port" 			: current_app.config.get("DB_PORT"),
		"db_name"           : current_app.config.get("DB_NAME"),
		"db_username"       : current_app.config.get("DB_USERNAME"),
	    "db_password"       : current_app.config.get("DB_PASSWORD")


	}

	return jsonify(res)