from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import current_app
from wingo.resources.util import SuccessResponse,ErrorResponse
from wingo.models import Note

# 'wingo' import must be done from root level (app, test, dbGen, ...)
#from models import Note
#from common.util import *


class TagResource(restful.Resource):
		
	def get(self):
		#Create args parsing 
		parser = reqparse.RequestParser()
		parser.add_argument('radius', type=int,help='Set a valid radius according to config',default=100)
		parser.add_argument('lat',    type=float, help='latitude should be a float', default=43.82186)
		parser.add_argument('lon',    type=float, help='latitude should be a float', default=43.82186)
		args = parser.parse_args()
		#Get args
		radius   = args["radius"]
		location = [args["lat"], args["lon"]]



		# notes = Note.objects(location__geo_within_center=[location,radius]).only("tags")

		#notes = Note.objects(location__near={"type": "Point", "coordinates": [0, 0]}).only("tags")
		
		notes = Note.objects(__raw__={'location':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance':radius}}}).only("tags")



		tags = set()
		
		#Get all uniq tags in a set 
		for note in notes:
			[tags.add(tag) for tag in note.tags]

		#Compute how many tags for each tags
		results = []
		for tag in tags:
			item = {"name":tag, "count":notes.filter(tags__contains=tag).count()}
			results.append(item)
			
 


		return SuccessResponse(sorted(results, key=lambda item: item["count"], reverse=True))
