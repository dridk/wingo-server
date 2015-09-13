from flask.ext.script import Manager , Shell
from wingo import create_app
from wingo import models
from wingo.utils import *
import unittest 
import os
import inspect 
from datetime import timedelta

#Create application
#try to use environ variable as config. Use by default devel
app = create_app(os.environ.get("WINGO_CONFIG","devel"))

# app.permanent_session_lifetime = timedelta(minutes=1)

manager = Manager(app, description="manage wingo application")

# def _make_context():
# 	return dict(User = models.User, Note = models.Note, Comm)
# manager.add_command("shell", Shell(make_context=_make_context))

@manager.command
def dropDatabase():
	''' Drop all database! This is a dangerous methods '''
	choice = input("Are you sure you want to drop all database ? [y/n]: ")
	if choice in ["yes","y", "YES"]:
		dropAll()
		print("database dropped ")


@manager.option('-lat', '--latitude', help='latitude of the center', default=48.386537, type=float)
@manager.option('-lon', '--longitude', help='longitude of the center', default=-4.490095, type=float)
@manager.option('-r', '--radius', help='radius in meter', default=5000)
@manager.option('-c', '--noteCount', help='number of note', default=100)
@manager.option('-u', '--userCount', help='number of user', default=3)
@manager.option('-v', '--verbose', help='show output', default=True)
def generate(latitude, longitude, radius, noteCount, userCount, verbose):
	''' Generate a new database and fill it with fake data ''' 

	choice = input("Are you sure you want to drop all database ? [y/n]: ")
	if choice in ["yes","y", "YES"]:
		genAll(latitude, longitude, radius, noteCount, userCount, verbose)
		print("database generated ")






if __name__ == "__main__":
	manager.run()