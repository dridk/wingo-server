from flask import jsonify, request 
from wingo.api_v1 import api 
from wingo.models import Comment

@api.route("/comments/", methods=['GET'])
def get_comments():
	return "not yet done"