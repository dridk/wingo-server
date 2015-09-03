from flask import Flask, jsonify, redirect, url_for
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
	#Connect to database 
	mongo.connect(app.config["DATABASE"])



	# register api blueprints 
	from wingo.api_v1 import api 
	app.register_blueprint(api, url_prefix='/api/v1')


	@app.route("/swagger")
	def root():
		return redirect(url_for('static', filename='swagger/index.html'))


	''' Get current user information  ''' 
	@app.route("/spec", methods=['GET'])
	@cross_origin()
	def spec():
		swag = swagger(app)
		swag['info']['version'] = "1.0"
		swag['info']['title'] = "My API"
		return jsonify(swag)




	return app 
