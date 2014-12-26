from flask import Flask
from flask import request
from flask import current_app
from flask.ext import restful
from flask.ext.restful import reqparse, abort
import hashlib
from bson.objectid import ObjectId
from bson.errors import *
from wingo.resources.util import SuccessResponse,ErrorResponse,check_auth,current_user
from wingo.models import Note, User, Comment


# 'wingo' import must be done from root level (app, test, dbGen, ...)
#from models import *
#from common.util import *
#import config



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# COMMENT COLLECTION 														#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class CommentCollection(restful.Resource):
	def get(self, note_id):
		""" GET handler for the request /notes/{id}/comments?page={page}
			Return the list comments of the note {id}
			page : int from 1 to max_int
		"""
		try:
			note = Note.objects.get(pk=note_id)
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Cannot find id")			


		results = []

		for comment in note.comments:
			r = {}
			r["id"] = str(comment.id)
			r["author"] = {"nickname":comment.author.nickname, "avatar" :comment.author.avatar }
			r["message"] = comment.message
			r["timestamp"]  = str(comment.timestamp)


			results.append(r)

		return SuccessResponse(results)

# ---------------------------------------------------------------------------
	@check_auth
	def post(self, note_id):
		""" POST handler for the request /notes/{id}/comments
			Register a new comment for the note {id}
		"""
		parser = reqparse.RequestParser()
		parser.add_argument('message', type=str, help='the comment', default=None)
		args = parser.parse_args()


		user = current_user()
		
		try:
			note = Note.objects.get(pk=note_id)
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Note doesn't exists")
		

		# # Create new comment
		comment = Comment();
		comment.author = user
		comment.message = args["message"]

		#Save comments....
		try:
			comment.save()
		except Exception as e:
			return ErrorResponse(e.message)

		#Save comment in notes
		try:
			note.comments.append(comment)
			print(note.comments)
			note.save()
		except Exception as e:
			return ErrorResponse(e.message)

		return SuccessResponse("yes")




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# COMMENT RESOURCE 															#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class CommentResource(restful.Resource):
	def get(self, comment_id):
		""" GET handler for the request /comments/{id}
			Return all details for the comment {id}
		"""
	
		try:
			comment = Comment.objects.get(pk=comment_id)
		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Comment doesn't exists")

		results  = dict()
		results["id"] = str(comment.id)
		results["author"] = {"nickname":comment.author.nickname, "avatar" :comment.author.avatar }
		results["message"] = comment.message
		results["timestamp"]  = str(comment.timestamp)
		

		return SuccessResponse(results)
		

# ---------------------------------------------------------------------------
	@check_auth
	def delete(self,comment_id):
		""" DELETE handler for the request /comments/{id}
			Delete the comment {id}
		"""
		try:
			comment = Comment.objects.get(id=comment_id)
			comment.delete()

		except InvalidId as e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Comment doesn't exists")
					
		return SuccessResponse()	



