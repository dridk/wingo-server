from wingo import create_app
from wingo.models import * 
from flask.ext.script import Manager
from dbtools.utils import *

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
	dropAll()


# @manager.option('-c', '--count', help='generate users ', default=1, type=int)
# def generate_user(int count):







@manager.option('-lat', '--latitude', help='latitude of the center', default=48.386537, type=float)
@manager.option('-lon', '--longitude', help='longitude of the center', default=-4.490095, type=float)
@manager.option('-r', '--radius', help='radius in meter', default=5000)
@manager.option('-c', '--noteCount', help='number of note', default=100)
@manager.option('-u', '--userCount', help='number of user', default=10)
@manager.option('-v', '--verbose', help='show output', default=True)
def generate(latitude, longitude, radius, noteCount, userCount, verbose):

	print("generate ")

	dropAll()

	
	for i in range(userCount):
		user = genUser()
		user.save()

		for j in range(noteCount):
			note = genNote(user,latitude=latitude , longitude= longitude, max_distance = radius)
			note.save()



