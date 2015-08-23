from flask import jsonify, request 
from wingo.api_v1 import api 
from wingo.models import User

@api.route("/users/", methods=['GET'])
def get_users():
	return jsonify({"nom":"sacha"})