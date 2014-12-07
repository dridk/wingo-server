from flask.ext.script import Manager
from wingo.application import app
from wingo.models import *
import random
from . utils import *
from progress.bar import *
from datetime import *

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
	Note.drop_collection()
	User.drop_collection()
    




@manager.option('-lat', '--latitude', help='latitude of the center', default=48.386537, type=float)
@manager.option('-lon', '--longitude', help='longitude of the center', default=-4.490095, type=float)
@manager.option('-r', '--radius', help='radius in meter', default=5000, type=int)
@manager.option('-c', '--count', help='number of note', default=100,type=int)
@manager.option('-u', '--userCount', help='number of user', default=10,type=int)
def generate(latitude, longitude, radius, count, userCount):
	"generate random notes at specific place"


	users = list()
	bar = Bar('Generating users...', max=userCount)
	for i in range(userCount):
		users.append(genUser())
		bar.next()
	bar.finish()


	bar = Bar('Generating note...', max=count)
	for i in range(count):
		pos = computeNewPointFrom(latitude, longitude, randint(0,359), randint(0,radius))
		note = Note()
		note.anonymous = random.choice([True,False])
		note.author = random.choice(users)
		note.message = "{} {}".format(genText(), genTags(random.randint(1,3)))
		note.location= list(pos)
		note.save()
		bar.next()
	bar.finish()
