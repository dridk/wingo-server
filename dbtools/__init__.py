from wingo import create_app
from wingo.models import * 
from flask.ext.script import Manager

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
	User.drop_collection()



@manager.option('-lat', '--latitude', help='latitude of the center', default=48.386537, type=float)
@manager.option('-lon', '--longitude', help='longitude of the center', default=-4.490095, type=float)
@manager.option('-r', '--radius', help='radius in meter', default=5000)
@manager.option('-c', '--count', help='number of note', default=100)
@manager.option('-u', '--userCount', help='number of user', default=10)
@manager.option('-v', '--verbose', help='show output', default=True)
def generate(latitude, longitude, radius, count, userCount, verbose):

	print("generate ")
	user = User(name="dridk", password="password", email="dridk@wingo.fr")
	user.save()

