from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse
from common.util import *
from models import Note

class NoteCollection(restful.Resource):
	def get(self):
		
		#http :5000/notes/search at==43.82186,-79.42456 radius==100

		
		#Create args parsing 
		parser = reqparse.RequestParser()
		parser.add_argument('radius', type=int, help='Rate cannot be converted', default=50)
		parser.add_argument('at', type=str, help='coordinate (at) must be defined', default=[43.82186,-79.42456])
		parser.add_argument('order', type=str, help='set recent or popular',choices=["recent","popular"], default="recent")
		parser.add_argument('query', type=str, help='add a keyword to searchg')

		args = parser.parse_args()


		print args["query"]




		#Get args
		radius   = args["radius"]
		order    = args["order"]
		location = [float(i) for i in args["at"].split(",")]
		query    = args["query"]

		print "radius:    {}".format(radius)
		print "latitude:  {}".format(location[0])
		print "longitude: {}".format(location[1])
		print "order    : {}".format(order)
		print "query    : {}".format(query)

		#Get notes
		if (order == "popular"):
			notes = Note.objects(location__near=location, location__max_distance=radius, tags__contains=query).order_by("takes")
		else:
			notes = Note.objects(location__near=location, location__max_distance=radius, tags__contains=query).order_by("timestamp")




		results = []
		for note in notes :
			r = dict()
			r["anonymous"]  = note.anonymous
			r["message"]    = note.message
			r["location"]   = note.location["coordinates"]
			r["expiration"] = str(note.expiration)
			r["timestamp"]  = str(note.timestamp)
			r["takes"]      = note.takes
			r["limit"]      =note.limit
			r["tags"]       =note.tags
			results.append(r)

		
		return SuccessResponse(results )
