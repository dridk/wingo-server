from flask.ext.script import Manager
from wingo.application import app
import unittest
import requests 
import json 
from dbtools.generate import *

manager = Manager(app)

@manager.command
def hello():
    print ("hello")

@manager.command
def run():
	app.run(debug=True, host="0.0.0.0")

@manager.command
def test():
	print("test")

@manager.command
def bench():
	print("bench")

@manager.option('-lat', '--latitude', help='latitude of the center')
@manager.option('-lon', '--longitude', help='longitude of the center')
@manager.option('-r', '--radius', help='radius in meter')
@manager.option('-v', '--verbose', help='show output')
def generate(latitude, longitude, radius, verbose):
	genDb(latitude, longitude, radius, verbose)

@manager.command
def reset():
	print("reset")


if __name__ == "__main__":
    manager.run()