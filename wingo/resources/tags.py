from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from common.util import *
from flask import current_app

class TagResource(restful.Resource):
		
	def get(self):
		#Create args parsing 
		parser = reqparse.RequestParser()
		parser.add_argument('radius', type=int,help='Set a valid radius according to config',default=50)
		args = parser.parse_args()

		return {"test":"bonjour"}
