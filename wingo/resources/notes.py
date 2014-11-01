from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from common.util import *
from models import *
import hashlib
from flask import current_app
from bson.objectid import ObjectId
from bson.errors import *
#======================================================================================================
class NoteCollection(restful.Resource):
	def get(self):
		
		#http :5000/notes at==43.82186,-79.42456 radius==100 order=recent query=cat
		#Create args parsing 
		parser = reqparse.RequestParser()
		parser.add_argument('radius', type=int, help='Set a valid radius according to config', 
			default=50)

		parser.add_argument('at', type=str, help='coordinate (at) must be defined', default="43.82186,-79.42456")
		parser.add_argument('order', type=str, help='set recent or popular',choices=["recent","popular"], default="recent")
		parser.add_argument('query', type=str, help='add a keyword to search', default=None)
		parser.add_argument('page', type=int, help='which page do you want')
		args = parser.parse_args()

		#Get args
		radius   = args["radius"]
		order    = args["order"]
		query    = args["query"]
		location = [float(i) for i in args["at"].split(",")]


		print "radius:    {}".format(radius)
		print "latitude:  {}".format(location[0])
		print "longitude: {}".format(location[1])
		print "order    : {}".format(order)
		print "query    : {}".format(query)

		#Get notes

		if query is None :
			if (order == "popular"):
				notes = Note.objects(location__near=location, location__max_distance=radius).order_by("-takes")
			else:
				notes = Note.objects(location__near=location, location__max_distance=radius).order_by("timestamp")

		else:
			if (order == "popular"):
				notes = Note.objects(location__near=location, location__max_distance=radius, tags__contains=query).order_by("-takes")
			else:
				notes = Note.objects(location__near=location, location__max_distance=radius, tags__contains=query).order_by("timestamp")



		results = []
		for note in notes :
			r = dict()

			if note.anonymous is False:
				r["author"] = {"nickname":note.author.nickname, "avatar" :note.author.avatar }
			r["id"]   		= str(note.id)
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

#======================================================================================================

	def post(self):
		#http POST :5000/notes at:=[43.82186,-79.42456] anonymous:=false -v

		parser = reqparse.RequestParser()
		parser.add_argument('author', type=str, help='user id')
		parser.add_argument('at', type=list, help='coordinate (at) must be defined', default="0,0")
		parser.add_argument('anonymous', type=bool, help='set anonymous true or false', default="true")
		parser.add_argument('picture', type=str, help='should be a link',default=None)
		parser.add_argument('message', type=str, help='add a keyword to searchg', default=None)
		parser.add_argument('expiration', type=str, help='set a date in format', default=None)
		parser.add_argument('limit', type=int, help='maximum takes',default=-1)
		args = parser.parse_args()

		note = Note();

		print args["at"]
		print type(args["at"])


		try:
			user = User.objects.get(id=args["author"])
		except:
			return ErrorResponse("user doesn't exists")
		
		note.author = user
		note.anonymous = args["anonymous"]
		note.picture=args["picture"]
		note.location  = args["at"]
		note.message = args["message"]

		try:
			note.save()
		except Exception, e:
			return ErrorResponse(e.message)

		return SuccessResponse(str(note.id))

#======================================================================================================

class NoteResource(restful.Resource):
	def get(self, note_id):

	
		try:
			note_id = ObjectId(note_id)
			note = Note.objects.get(pk=note_id)
		except InvalidId, e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")			

		results  = dict()
		if note.anonymous is False:
			results["author"] = {"nickname":note.author.nickname, "avatar" :note.author.avatar }

		results["anonymous"]  = note.anonymous
		results["message"]    = note.message
		results["location"]   = note.location["coordinates"]
		results["expiration"] = str(note.expiration)
		results["timestamp"]  = str(note.timestamp)
		results["takes"]      = note.takes
		results["limit"]      =note.limit
		results["tags"]       =note.tags


		
		return SuccessResponse(results)


		

#======================================================================================================
	def delete(self,note_id):
		note_id = ObjectId(note_id)
		try:
			note_id = ObjectId(note_id)
			note = Note.objects.get(id=note_id)
			note.delete()
		except InvalidId, e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")	

					
		return SuccessResponse()	






#======================================================================================================