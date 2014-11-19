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

		email    = args["email"]
		password = args["password"]
		user = User.objects(email=email, password=password).first()
	
		if user is None:
			return ErrorResponse("Bas email or password")

		else:
			session['user_id'] = str(user.id)

		return SuccessResponse(session['user_id'])
		



class UserLogout(restful.Resource):
	def delete(self):
		print("delete session",session["user_id"])
		session.pop("user_id", None)
		print(session)

		return SuccessResponse()



class UserMe(restful.Resource):
	def get(self):

		print(session)

		
		if 'user_id' in session:
			user = User.from_id(session["user_id"])

			results = {}
			results["email"] = user.email
			results["nickname"] = user.nickname
			results["avatar"] = user.avatar
			return SuccessResponse(results)
		else:
			return ErrorResponse("not connected")


class UserNote(restful.Resource):
	
	''' get all user's note '''
	def get(self):
		pass 

	''' Add a notes to the current user pockets'''
	''' add note_id in posted data '''
	def post(self):
		pass	
	


