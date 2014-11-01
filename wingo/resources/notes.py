from flask import Flask
from flask import request
from flask.ext import restful
from common.util import *
from models import Note

class NoteCollection(restful.Resource):
	def get(self):
		#http :5000/notes/search?at=43.82186,-79.42456&radius=1000

		location = request.args.get('at').split(",")
		radius   = int(request.args.get("radius", 50))
		
		location = [float(i) for i in location]


		notes = Note.objects(location__near=location, location__max_distance=radius)	

		results = []
		for note in notes :
			r = dict()
			r["anonymous"]  = note.anonymous
			r["message"]    = note.message
			r["location"]   = note.location
			r["expiration"] = str(note.expiration)
			r["timestamp"]  = str(note.timestamp)
			r["takes"]      = note.takes
			r["limit"]      =note.limit
			r["tags"]       =note.tags
			
			results.append(r)

		return SuccessResponse(results )
