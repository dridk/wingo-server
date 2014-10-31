
from loremipsum import *
from random import randint
from wingo.models import *

print("GENERATE DATABASE ... ")
connect('wingo') 
#CREATE USERS 
# Looks.. all users nickname start by "i" :D

User.drop_collection()
User(email="sacha@labsquare.org",
	password="pass",
	nickname="idok").save()

User(email="gueudelotolive@gmail.com",
	password="pass",
	nickname="ikit").save()


User(email="eugene.trounev@gmail.com",
	password="pass",
	nickname="it-s").save()


#CREATE Notes 
# Looks.. all users nickname start by "i" :D

Note.drop_collection()
#Simple function to generate 255 txt.
def genText():
	txt = get_paragraph()
	if len(txt)>255:
		return txt[0:255]
	else:
		return txt

#http://universimmedia.pagesperso-orange.fr/geo/loc.htm
defautLocation = [
[43.82186,-79.42456],
[43.81877,-79.42172],
[43.82061,-79.42814],
[43.82375,-79.42621],
[43.82928,-79.42760]
]
defautUser = User.objects.first()


for loc in defautLocation:
	note = Note()
	note.author = defautUser
	note.message = genText()
	note.location=loc
	note.takes = randint(0,300)
	note.save()





