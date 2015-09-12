from flask import jsonify, request, url_for, current_app
from wingo.api_v1 import api 
from wingo.utils import toJson
from wingo.models import Comment, Note
from wingo.exceptions import CustomError


#=====================================================
@api.route("/notes/<id>/comments", methods=['GET'])
def get_comments_list(id):
	""" 
	Get comment list from a note
	---
	tags:
		- comments 
	parameters:
		- name: id
		  in: path
		  description: note id 
		  required: true
		  type: string
	"""
	note  = Note.objects(pk=id).first()
	items = [i.export_data() for i in note.comments]
	return toJson(items)

#=====================================================

@api.route("/notes/<string:note_id>/comments/<int:comment_id>", methods=['GET'])
def get_comment(note_id, comment_id):
	""" 
	Get comment from note  
	---
	tags:
		- comments 
	parameters:
		- name: note_id
		  in: path 
		  description: note id 
		  required: true 
		  type: string 
		- name: comment_id
		  in: path 
		  description: comment id 
		  required: true 
		  type: integer 
	"""
	note = Note.objects.get(pk = note_id)
	if comment_id >= len(note.comments):
		raise CustomError("comment id out of range")
	return toJson(note.comments[comment_id].export_data())

#=====================================================

@api.route("/notes/<id>/comments", methods=['POST'])
def create_comment(id):
	""" 
	Create a comment  
	---
	tags:
		- comments 
	parameters:
		- name: id 
		  in: path 
		  description: note id 
		  required: true 
		  type: string
		- in: body 
		  name: body 
		  schema:
		  	id: Comment 
		  	required:
		  		- message
		  		- author 
		  	properties:
		  		message:
		  			type: string
		  			description: message 
		  		author: 
		  			type: string
		  			description: author id 
	"""
	note = Note.objects.get(pk = id);
	comment = Comment()
	comment.import_data(request.json)
	note.comments.append(comment)
	note.save()
	return toJson({"id": str(note.id)})