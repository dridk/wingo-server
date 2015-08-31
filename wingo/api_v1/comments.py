from flask import jsonify, request, url_for, current_app
from wingo.api_v1 import api 
from wingo.utils import toJson
from wingo.models import Comment, Note



@api.route("/notes/<id>/comments/", methods=['GET'])
def get_comments_list(id):
	
	note  = Note.objects(pk=id).first()
	items = [i.export_data() for i in note.comments]
	return toJson(items)


@api.route("/notes/<note_id>/comments/<int:comment_id>/", methods=['GET'])
def get_comment(note_id, comment_id):
	note = Note.objects.get(pk = note_id)
	return toJson(note.comments[comment_id].export_data())


@api.route("/notes/<id>/comments/", methods=['POST'])
def create_comment(id):
	note = Note.objects.get(pk = id);
	comment = Comment()
	comment.import_data(request.json)
	note.comments.append(comment)
	note.save()
	return toJson({"id": str(note.id)})