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
import requests
import werkzeug 
import uuid, base64
from geopy.geocoders import Nominatim 
import json




class LocationHereResource(restful.Resource):
	''' Get current location as a string name '''
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('lat',       type=float, help='lat is missing or not well defined ',required=True)
		parser.add_argument('lon',       type=float, help='long is missing or not well defined', required=True)
		args = parser.parse_args()
		at = "{},{}".format(args["lat"], args["lon"])
	
		app_id = current_app.config["HERE_APP_ID"]
		app_code = current_app.config["HERE_APP_CODE"]

		data = {"at":at, "app_id":app_id, "app_code":app_code}


		r = requests.get("http://places.cit.api.here.com/places/v1/discover/here", params=data)
		results = r.json().get("results")
		if len(results["items"]) > 0:
			if "vicinity" in results["items"][0]:
				return SuccessResponse(results["items"][0]["vicinity"])
		
		return SuccessResponse("Unknown location")

	
		


class LocationArroundResource(restful.Resource):
	''' Get current location as a string name '''
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('lat',       type=float, help='lat is missing or not well defined ',required=True)
		parser.add_argument('lon',       type=float, help='long is missing or not well defined', required=True)
		args = parser.parse_args()
		

		at = "{},{}".format(args["lat"], args["lon"])
		app_id = current_app.config["HERE_APP_ID"]
		app_code = current_app.config["HERE_APP_CODE"]

		data = {"at":at, "app_id":app_id, "app_code":app_code}

		r = requests.get("http://places.cit.api.here.com/places/v1/discover/explore", params=data)

		results = []

		for item in r.json().get("results").get("items"):
			line = {}
			line["title"] = item["title"]
			line["distance"] = item["distance"]
			line["icon"] = item["icon"]
			line["latitude"] = item["position"][0]
			line["longitude"] = item["position"][1]
			results.append(line)

		return SuccessResponse(results)




