from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse, abort
from common.util import *
import hashlib
from flask import current_app
from bson.objectid import ObjectId
from bson.errors import *

import config
from models import *




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# COMMENT COLLECTION 														#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class CommentCollection(restful.Resource):
	def get(self, note_id):
		""" GET handler for the request /notes/{id}/comments?page={page}
			Return the list comments of the note {id}
			page : int from 1 to max_int
		"""
		#http :5000/notes/54558058a5dec553a9aa50b9/comments

		# Retrieve the note and all its comments
		try:
			note_id = ObjectId(note_id)
			note = Note.objects.get(pk=note_id)
		except InvalidId, e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Note doesn't exists")


		# Pagination
		parser = reqparse.RequestParser()
		parser.add_argument('page', type=int, help='the page', default=1)
		args = parser.parse_args()

		countElement = 10
		startPage    = args["page"]
		startElement = (args["page"] - 1) * countElement

		if config.DEBUG:
			print "note id      : {0}".format(note_id)
			print "startElement : {0}".format(startElement)
			print "countElement : {0}".format(countElement)
			print "startPage    : {0}".format("-")


		# Build result
		results  = dict()
		results["startElement"] = startElement
		results["startPage"]    = 1
		results["countElement"] = countElement
		results["comments"]     = dict()


		for idx, comment in enumerate(note.comments):
			if idx < startElement:
				continue
			if idx > startElement + countElement:
				break
			results["comments"].append(comment)

		
		return SuccessResponse(results)



# ---------------------------------------------------------------------------

	def post(self, note_id):
		""" POST handler for the request /notes/{id}/comments
			Register a new comment for the note {id}
		"""
		#http POST :5000/notes/54558058a5dec553a9aa50b9/comments
		# TODO : [security] avoid code injection

		parser = reqparse.RequestParser()
		parser.add_argument('author', type=str, help='user id')
		parser.add_argument('comment', type=str, help='the comment', default=None)
		args = parser.parse_args()


		if config.DEBUG:
			print "note id : {0}".format(note_id)
			print "author  : {0}".format(args["author"])
			print "comment : {0}".format(args["comment"][0:50] + "(...)")


		# Check that user and note exists
		try:
			user = User.objects.get(id=args["author"])
		except:
			return ErrorResponse("User doesn't exists")
		try:
			note_id = ObjectId(note_id)
			note = Note.objects.get(pk=note_id)
		except InvalidId, e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Note doesn't exists")
		

		# Create new comment
		comment = Comment();
		comment.author = user
		comment.note = note
		comment.comment = args["comment"]

		try:
			comment.save()
		except Exception, e:
			return ErrorResponse(e.message)

		return SuccessResponse(str(comment.id))




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# COMMENT RESOURCE 															#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class CommentResource(restful.Resource):
	def get(self, comment_id):
		""" GET handler for the request /comments/{id}
			Return all details for the comment {id}
		"""
	
		try:
			comment_id = ObjectId(comment_id)
			comment = Comment.objects.get(pk=comment_id)
		except InvalidId, e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Comment doesn't exists")


		if config.DEBUG:
			print "comment id : {0}".format(comment_id)


		results  = dict()
		results["comment"] = comment.comment
		results["author"]  = comment.author
		results["date"]    = comment.date
		

		return SuccessResponse(results)
		

# ---------------------------------------------------------------------------

	def delete(self,comment_id):
		""" DELETE handler for the request /comments/{id}
			Delete the comment {id}
		"""

		try:
			comment_id = ObjectId(comment_id)
			comment = Comment.objects.get(id=comment_id)
			comment.delete()

			if config.DEBUG:
				print "Comment (id ={0}) deleted".format(comment_id)

		except InvalidId, e:
			return ErrorResponse(e.message)
		except:
			return ErrorResponse("Comment doesn't exists")
					
		return SuccessResponse()	



