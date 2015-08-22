from flask import Flask, jsonify


def create_app(config_name):

	app = Flask(__name__)

	return app 
