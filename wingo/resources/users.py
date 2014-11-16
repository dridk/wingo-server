from flask import Flask
from flask import request
from flask import session
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import current_app
# from flask_login import login_user, current_user 

from . util import SuccessResponse,ErrorResponse
from models import User
# 'wingo' import must be done from root level (app, test, dbGen, ...)
#from models import Note
#from common.util import *


class UserLogin(restful.Resource):
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('email',    type=str,   help='email is not defined', required = True)
		parser.add_argument('password',    type=str,   help='Password is not defined', required = True)
		
		args = parser.parse_args()

		email = args["email"]
		password = args["password"]
		user = User.objects(email=email, password=password).first()
	
		if user is None:
			return ErrorResponse("Bas email or password")

		else:
			session['user'] = "sadsfsfsf"

		return SuccessResponse()
		



class UserLogout(restful.Resource):
	def post(self):
		return "logout"


class UserMe(restful.Resource):
	def get(self):
		print(session)
		if "current_user_id" not in session:
			return ErrorResponse("not logged")
		else:
			return SuccessResponse(session["current_user_id"])


class UserNote(restful.Resource):
	
	''' get all user's note '''
	def get(self):
		pass 

	''' Add a notes to the current user pockets'''
	''' add note_id in posted data '''
	def post(self):
		pass	
	


