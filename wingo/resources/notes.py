from flask import Flask
from flask import request
from flask import current_app
from flask.ext import restful
from flask import send_file
import os
from flask.ext.restful import reqparse, abort
from flask import make_response, redirect
from bson.objectid import ObjectId
from bson.errors import *
import hashlib
from wingo.resources.util import SuccessResponse,ErrorResponse,check_auth, current_user
from wingo.models import Note, User, PocketNote
import werkzeug 
import uuid, base64
import requests
import io
# 'wingo' import must be done from root level (app, test, dbGen, ...)
# It doesnt' work instead ! 
#from common.util import *
#from models import *



#======================================================================================================
class NoteCollection(restful.Resource):
	def get(self):
		
		#http :5000/notes at==43.82186,-79.42456 radius==100 order=recent query=cat
		#Create args parsing 
		parser = reqparse.RequestParser()
		parser.add_argument('radius',type=int,   help='Set a valid radius', default=50)
		parser.add_argument('lat',   type=float, help='lat is missing or not well defined ', default=43.82186)
		parser.add_argument('lon',   type=float, help='long is missing or not well defined', default=-79.42456)
		parser.add_argument('order', type=str,   help='order is missing[recent or popular]',choices=["recent","popular"], default="recent")
		parser.add_argument('query', type=str,   help='query is missing', default=None)
		parser.add_argument('max_id', type=str,   help='pagination max_id', default=None)

		args = parser.parse_args()

		#Get args
		radius   = args["radius"]
		order    = args["order"]
		query    = args["query"]
		lat      = args["lat"]
		lon      = args["lon"]
		max_id   = args["max_id"]
		location = [lat,lon]
		
		print ("radius:    {}".format(radius))
		print ("latitude:  {}".format(lat))
		print ("longitude: {}".format(lon))
		print ("order:     {}".format(order))
		print ("query:     {}".format(query))
		print ("max_id:    {}".format(max_id))

		# count_per_page = current_app.config["COUNT_PER_PAGE"]
		count_per_page =10

		#Get notes

		# if query is None :
		# 	if (order == "popular"):
		# 		notes = Note.objects(__raw__={'location':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance':radius}}}).order_by("-takes").limit(count_per_page)
		# 	else:

		
		if max_id is None:
			notes = Note.objects(__raw__={'location':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance':radius}}}).order_by("-timestamp").limit(count_per_page)
		else:
			notes = Note.objects(__raw__={'_id':{'$lt': ObjectId(max_id)},  'location':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance':radius}}}).order_by("-timestamp").limit(count_per_page)

		# else:
		# 	if (order == "popular"):
		# 		notes = Note.objects(__raw__={'tags':query, 'location':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance':radius}}}).order_by("-takes").limit(count_per_page)
		# 	else:
		# 		notes = Note.objects(__raw__={'tags':query,'location':{'$near':{'$geometry':{'type': "Point", 'coordinates': location},'$maxDistance':radius}}}).order_by("-timestamp").limit(count_per_page)



		results = []
		for note in notes :
			r = dict()

			if note.anonymous is False:
				r["author"] = {"nickname":note.author.nickname, "avatar" :note.author.avatar }
				
			r["id"]   		= str(note.id)
			r["anonymous"]  = note.anonymous
			r["message"]    = note.message
			r["lat"]        = float(note.location["coordinates"][0])
			r["lon"]       = float(note.location["coordinates"][1])
			r["expiration"] = str(note.expiration)
			r["timestamp"]  = str(note.timestamp)
			r["takes"]      = note.takes
			r["limit"]      =note.limit
			r["tags"]       =note.tags
			r["picture"]    = note.picture

			results.append(r)

		if len(results) > 0:
			return SuccessResponse(results, max_id = results[-1]["id"], count_per_page=count_per_page)

		return SuccessResponse(results)

#======================================================================================================
	@check_auth
	def post(self):
		#http POST :5000/notes at:=[43.82186,-79.42456] anonymous:=false -v

		parser = reqparse.RequestParser()
		parser.add_argument('author',    type=str,   help='Author is not defined')
		parser.add_argument('lat',       type=float, help='lat is missing or not well defined ',required=True)
		parser.add_argument('lon',       type=float, help='long is missing or not well defined', required=True)
		parser.add_argument('anonymous', type=bool,  help='set anonymous true or false', default=True)
		parser.add_argument('picture',   type=str,   help='picture link is wrong')
		parser.add_argument('message',   type=str,   help='message is missing', required=True)
		parser.add_argument('expiration',type=str,   help='expiration is not well defined')
		parser.add_argument('limit',     type=int,   help='limit is not well defined',default=-1)


		
		args = parser.parse_args()
	

		note = Note();

		
		# print "author:    {}".format(args["author"])
		# print "latitude:  {}".format(args["lat"])
		# print "longitude: {}".format(args["lon"])
		# print "anonymous: {}".format(args["anonymous"])
		# print "picture:   {}".format(args["picture"])
		# print "message:   {}".format(args["message"])
		# print "expiration:{}".format(args["expiration"])
		# print "limit:     {}".format(args["limit"])


		
		note.author    = current_user()
		note.anonymous = args["anonymous"]
		note.picture   = args["picture"]
		note.location  = [args["lat"], args["lon"]]
		note.message   = args["message"]
		
		try:
			note.save()
		except Exception as e:
			return ErrorResponse(e.message)

		return SuccessResponse(str(note.id))

#======================================================================================================

class NoteResource(restful.Resource):
	def get(self, note_id):

	
		try:
			note = Note.objects.get(pk=note_id)
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")			

		results  = dict()
		if note.anonymous is False:
			results["author"] = {"nickname":note.author.nickname, "avatar" :note.author.avatar }

		results["anonymous"]  = note.anonymous
		results["message"]    = note.message
		results["message"]    = note.message
		results["lat"]   = note.location["coordinates"][0]
		results["lon"]   = note.location["coordinates"][1]
		results["expiration"] = str(note.expiration)
		results["timestamp"]  = str(note.timestamp)
		results["takes"]      = note.takes
		results["limit"]      =note.limit
		results["tags"]       =note.tags
		results["picture"]    =note.picture



		
		return SuccessResponse(results)


		

#======================================================================================================
	def delete(self,note_id):
		
		try:
			note_id = ObjectId(note_id)
			note = Note.objects.get(id=note_id)
			note.delete()
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")	

					
		return SuccessResponse()	


#======================================================================================================

class NoteUploadResource(restful.Resource):
	def post(self):
	 	#http -f POST :5000/notes/upload picture@/home/schutz/cv.png


		file = request.files["picture"]


		if file and self.allowed_file(file.filename):
			filename = werkzeug.secure_filename(file.filename)
			ext = filename.rsplit('.', 1)[1]
			uid = uuid.uuid4().hex
			newName = str(uid) + "." + ext
			file.save(os.path.join(current_app.config["UPLOAD_FOLDER"],newName))
			newUrl = "http://"+request.headers['Host']+"/pics/"+newName
			return SuccessResponse({"path":newUrl})

		else :
			return ErrorResponse("File are not allowed")


	def allowed_file(self,filename):
	    return '.' in filename and \
	           filename.rsplit('.', 1)[1] in current_app.config["UPLOAD_ALLOWED_EXTENSIONS"]


class NoteDownloadResource(restful.Resource):
	def get(self, filename):
		#In production, should be appear on nginx static folder...
		filename = os.path.join(current_app.config["UPLOAD_FOLDER"],filename)


		if os.path.exists(filename): 
			return send_file("../"+filename, mimetype="image/png")
		else:
			return ErrorResponse("image doesn't exists")


#======================================================================================================


class PocketNoteCollection(restful.Resource):	
	''' get all user's note '''
	@check_auth
	def get(self):
		user = current_user()
		results  = list()
		for note in user.pockets:
			r = {}
			r["message"]    = note.message
			r["lat"]   = note.location["coordinates"][0]
			r["lon"]   = note.location["coordinates"][1]
			r["timestamp"]  = str(note.timestamp)
			r["signature"]  = note.signature

			r["parent"]   = str(note.parent)
			results.append(r)

		return SuccessResponse(results)


	''' Add a notes to the current user pockets'''
	''' add note_id in posted data '''
	@check_auth
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('note_id',type=str,   help='Specify note uniq id', required=True)		
		args = parser.parse_args()
		note_id = ObjectId(args["note_id"])

		#Get the defined notes
		note = Note.objects(id=note_id).first()
		print("current note: ", note)

		#Get the current user
		user = current_user()
		print("current user: ", user)

		# If user has already the note, return error 
		if user.has_note(note):
			return ErrorResponse("User has already this note")

		# Appends pocketNotes to the users
		user.pockets.append(PocketNote.from_note(note))
		
		# Save all modification
		try:
			user.save()
		except Exception as e:
			return ErrorResponse("cannot save into user pokets")

		try:
			note.save()
		except Exception as e:
			return ErrorResponse("cannot increments note takes count")

		
		results = {"takes": len(user.pockets)}
		return SuccessResponse(results)


class PocketNoteResource(restful.Resource):
	
	def delete(self,note_id):
		try:
			note_id = ObjectId(note_id)
			note = Note.objects.get(id=note_id)
			note.delete()
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")	

					
		return SuccessResponse()	



	
#=================================================MY NOTES ============================================

class MyNoteCollection(restful.Resource):	
	''' get all user's note '''
	@check_auth
	def get(self):
	
		user           = current_user()
		results        = list()

		for note in Note.objects(author=user):
			r = {}
			if note.anonymous is False:
				r["author"] = {"nickname":note.author.nickname, "avatar" :note.author.avatar }
				
			r["id"]   		= str(note.id)
			r["anonymous"]  = note.anonymous
			r["message"]    = note.message
			r["lat"]        = float(note.location["coordinates"][0])
			r["lon"]        = float(note.location["coordinates"][1])
			r["expiration"] = str(note.expiration)
			r["timestamp"]  = str(note.timestamp)
			r["takes"]      = note.takes
			r["limit"]      = note.limit
			r["tags"]       = note.tags
			r["picture"]    = note.picture
			results.append(r)

		return SuccessResponse(results)




#======================================================================================================

class NoteMapResource(restful.Resource):	
	''' get static map of the current note'''
	def get(self, note_id):

		#This method should be have cache , to avoid requests Here each time

		app_id   = current_app.config["HERE_APP_ID"]
		app_code = current_app.config["HERE_APP_CODE"]

		try:
			note = Note.objects.get(pk=note_id)
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")	

		at= "{},{}".format(note.location["coordinates"][0], note.location["coordinates"][1])		
		data = {"c":at, "w":600, "h":600,"app_id":app_id, "app_code":app_code, "z":16}

		r = requests.get("http://image.maps.cit.api.here.com/mia/1.6/mapview", params=data)

		#should be update with StringIO...Don't know optimisation of this... 
		rep = make_response(r.content)
		rep.headers['Content-Type'] = 'image/jpeg'

		return rep
		



