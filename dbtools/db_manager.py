from flask.ext.script import Manager
from wingo.application import app
from wingo.models import *
import random
from . utils import *
from progress.bar import *
from datetime import *
import os
import shutil

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
	Note.drop_collection()
	User.drop_collection()
    




@manager.option('-lat', '--latitude', help='latitude of the center', default=43.8174759, type=float)
@manager.option('-lon', '--longitude', help='longitude of the center', default=-79.4210148, type=float)
@manager.option('-r', '--radius', help='radius in meter', default=5000, type=int)
@manager.option('-c', '--count', help='number of note', default=100,type=int)
@manager.option('-u', '--userCount', help='number of user', default=10,type=int)
def generate(latitude, longitude, radius, count, userCount):
	"generate random notes at specific place"


	users  = list()
	photos = ["http://www.toulon-hyeres.aeroport.fr/var/storage/images/media/images/bes12/13851-1-fre-FR/bes1.jpg",
			  "http://knightsinntoronto-com.factorepreview.ca/system/images/images/2/original/toronto-012222.jpg?1358279327"]
	
	# Add default dev user 
	devUser = User(email="sacha@labsquare.org",
					  password="sacha",
					  nickname="dridk", 
					  avatar="http://www.gravatar.com/avatar/2381d1dbfc1450b861bd808424d01943?s=48&d=identicon")
	devUser.save()


		# Add default dev user 
	devUser = User(email="eugene@labsquare.org",
					  password="eugene",
					  nickname="it-s", 
					  avatar="http://www.gravatar.com/avatar/da5261bbb6144dafb2517b669800b565?s=90&d=identicon")
	devUser.save()

			# Add default dev user 
	devUser = User(email="olivier@labsquare.org",
					  password="olvier",
					  nickname="ikit", 
					  avatar="http://www.gravatar.com/avatar/c210cfde7065e9f2a0d184e629013488?s=90&d=identicon")
	devUser.save()




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
		if random.randint(1, 5) == 1:
			note.picture = random.choice(photos)
		note.save()
		bar.next()
	bar.finish()
