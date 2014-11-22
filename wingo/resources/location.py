from flask import Flask
from flask import request
from flask import current_app
from flask.ext import restful
from flask import send_file
import os
from flask.ext.restful import reqparse, abort
from bson.objectid import ObjectId
from bson.errors import *
import hashlib
from . util import SuccessResponse,ErrorResponse,check_auth, current_user
from models import Note, User, PocketNote
import werkzeug 
import uuid, base64
from geopy.geocoders import Nominatim 




class LocationHereResource(restful.Resource):
	''' Get current location as a string name '''
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('lat',       type=float, help='lat is missing or not well defined ',required=True)
		parser.add_argument('lon',       type=float, help='long is missing or not well defined', required=True)
		args = parser.parse_args()
		at = "{},{}".format(args["lat"], args["lon"])
		geolocator = Nominatim()
		location = geolocator.reverse(at)
		return SuccessResponse(location.address)
		


class LocationArroundResource(restful.Resource):
	''' Get current location as a string name '''
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('lat',       type=float, help='lat is missing or not well defined ',required=True)
		parser.add_argument('lon',       type=float, help='long is missing or not well defined', required=True)
		args = parser.parse_args()
		return "map"


