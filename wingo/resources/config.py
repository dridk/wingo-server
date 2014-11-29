from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import current_app
from wingo.resources.util import SuccessResponse,ErrorResponse


# 'wingo' import must be done from root level (app, test, dbGen, ...)
#from common.util import *


class ConfigResource(restful.Resource):
	def get(self):
		results = {
		"version":current_app.config["VERSION"],
		"name":current_app.config["VERSION_NAME"],
		"allowed_radius":current_app.config["ALLOWED_RADIUS"],
		"max_note_length":current_app.config["MAX_NOTE_LENGTH"]
		}

		return SuccessResponse(results)