from flask import Flask
from flask import request
from flask.ext import restful
from common.util import *
from models import Note

class NoteCollection(restful.Resource):
	def get(self):
		#http :5000/notes/search?at=43.8,-79

		location = request.args.get('at').split(",")
		print location
		notes = Note.objects(location__near=location, location__max_distance=50)
		
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

		return SuccessResponse(results)
