from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from common.util import *
from flask import current_app


class ConfigResource(restful.Resource):
	def get(self):
		results = {
		"version":current_app.config["VERSION"],
		"name":current_app.config["VERSION_NAME"],
		"allowed_radius":current_app.config["ALLOWED_RADIUS"],
		"max_note_length":current_app.config["MAX_NOTE_LENGTH"]
		}


	return results