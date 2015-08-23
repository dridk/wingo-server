from flask import Flask, jsonify
import mongoengine as mongo 
from wingo.models import *

def create_app(config_name):

	app = Flask(__name__)
	mongo.connect("wingo")

	# register blueprints 

	from wingo.api_v1 import api 
	app.register_blueprint(api, url_prefix='/api/v1')



	return app 
