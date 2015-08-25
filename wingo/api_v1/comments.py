from flask import jsonify, request, url_for, current_app
from wingo.api_v1 import api 
from wingo.models import Comment


@api.route("/index/")
def home():
	return "home"

@api.route("/comments/", methods=['GET'])
def get_comments():
	return  url_for('api.home')