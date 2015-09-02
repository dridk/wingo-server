from flask import Flask, jsonify
import mongoengine as mongo
import os 
from wingo.models import *

def create_app(config_name):
	""" 
	Create and return application instance ,
	setup database and load configuration 
	"""

	#Get config path 
	cfg = os.path.join(os.getcwd(),"config",config_name + ".py")

	#Create Application instance and set configuration
	app = Flask(__name__)
	app.config.from_pyfile(cfg)

	#Connect to database 
	mongo.connect(app.config["DATABASE"])


	print("CONFIG NAME ",config_name)

	# register api blueprints 
	from wingo.api_v1 import api 
	app.register_blueprint(api, url_prefix='/api/v1')



	return app 
