from flask import Flask, jsonify, redirect, url_for, render_template, request
import mongoengine as mongo
import os 
from wingo.models import *
from flask.ext.cors import CORS, cross_origin
from flask_swagger import swagger

def create_app(config_name):
	""" 
	Create and return application instance ,
	setup database and load configuration 
	"""

	#Get config path 
	cfg = os.path.join(os.getcwd(),"config",config_name + ".py")

	#Create Application instance and set configuration
	app = Flask(__name__, static_url_path='')
	app.config.from_pyfile(cfg)
	cors = CORS(app)
	app.config['CORS_HEADERS'] = 'Content-Type'
	app.config["CONFIG_NAME"]  = config_name
	#Connect to database 
	# mongo.connect(app.config["DB_NAME"],
	# 			  host     = app.config["DB_HOST"],
	# 			  port     = app.config["DB_PORT"],
	# 			  username = app.config["DB_USERNAME"],
	# 			  password = app.config["DB_PASSWORD"]) 


	mongo.connect("wingo",
				  host     = "10.0.113.75",
				  port     = 49415,
				  username = "admin",
				  password = "5JaRSxwTsTs4TZthRRsHXqLH") 



	# register api blueprints 
	from wingo.api_v1 import api 
	app.register_blueprint(api, url_prefix='/api/v1')


	@app.route("/")
	def root():
		print("SACHA", request.url_root)
		return render_template("index.html", url_root = request.url_root+"/spec")


	''' Get current user information  ''' 
	@app.route("/spec", methods=['GET'])
	@cross_origin()
	def spec():
		swag = swagger(app)
		swag['info']['version'] = "1.0"
		swag['info']['title'] = "My API"
		return jsonify(swag)




	return app 
