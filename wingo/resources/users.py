from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import current_app
from . util import SuccessResponse,ErrorResponse
from models import Note
from app import app

# 'wingo' import must be done from root level (app, test, dbGen, ...)
#from models import Note
#from common.util import *







class UserNote(restful.Resource):
	
	''' get all user's note '''
	def get(self):
		pass 

	''' Add a notes to the current user pockets'''
	''' add note_id in posted data '''
	def post(self):
		pass	
	


