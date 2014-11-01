from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from common.util import *
from flask import current_app

from models import Note


class TagResource(restful.Resource):
		
	def get(self):
		#Create args parsing 
		parser = reqparse.RequestParser()
		parser.add_argument('radius', type=int,help='Set a valid radius according to config',default=100)
		parser.add_argument('at', type=str, help='coordinate (at) must be defined', default="43.82186,-79.42456")

		args = parser.parse_args()
		#Get args
		radius   = args["radius"]
		location = [float(i) for i in args["at"].split(",")]



		notes = Note.objects(location__near=location, location__max_distance=radius).only("tags")
		tags = set()
		
		#Get all uniq tags in a set 
		for note in notes:
			[tags.add(tag) for tag in note.tags]

		#Compute how many tags for each tags
		results = []
		for tag in tags:
			item = {"name":tag, "count":notes.filter(tags__contains=tag).count()}
			results.append(item)


		return SuccessResponse(sorted(results, reverse=True))
