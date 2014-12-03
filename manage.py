from flask.ext.script import Manager
from wingo.application import app
import unittest
import requests 
import json 
import dbtools.db_manager as db

manager = Manager(app, description="manage wingo application")
manager.add_command("dbtools", db.manager)

@manager.command
def hello():
	"Says hello"
	print ("hello")



if __name__ == "__main__":
    manager.run()