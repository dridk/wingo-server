from flask import jsonify
from wingo.models import *
from webargs import Arg
from loremipsum import *
import math
from datetime import *
from random import randint
import requests


#=================================================================================
def toJson(data):
	''' Convert Python data to Json response '''

	if isinstance(data, list):
		return jsonify({"success":True, "results":data, "total":len(data)})
	else:
		return jsonify({"success":True, "results": data})

#=================================================================================

def selectNotes(center, radius = 10000 , search = None):
	''' Select note from coordinate ''' 
	if search is None: 
		queryset = 	Note.objects(location__near=center , location__max_distance=radius)
	else:
		queryset =  Note.objects(location__near=center , location__max_distance=radius, tags__contains=search)
	return queryset


#=================================================================================

def genText(maxLen=100):
	'''
	To generate 255 txt 
	:param maxLen: the length of message 
	:return: random text
	'''
	return get_paragraph()[:maxLen].replace("'","")

#=================================================================================

def dropAll():
	''' Drop all database ''' 
	try:
		User.drop_collection()
		Note.drop_collection()
	except :
		print("cannot drop. No table")

#=================================================================================

def computeNewPointFrom(lat, lon, bearing, distance):
	'''
	To generate a new position from a start position, an angle and a distance (lat/lon, degree, meter)
	:param lat: latitude of the center
	:param lon: longitude of the center 
	:param bearing: direction from the center
	:param distance: distance from the centr
	:return: a tuple (latitude, longitude)
	'''
	#constants
	dR = (distance / 1000.0) / 6373.0
	deg2rad = math.pi/180.0

	# convert angle in radian
	lat1 = lat * deg2rad
	lon1 = lon * deg2rad
	brng = bearing * deg2rad

	lat2 = math.asin( math.sin(lat1) * math.cos(dR) + math.cos(lat1) * math.sin(dR) * math.cos(brng) )
	lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(dR) * math.cos(lat1), math.cos(dR) - math.sin(lat1) * math.sin(lat2))

	# convert back to degree
	rad2deg = 180.0 / math.pi
	return (lat2 * rad2deg, lon2 * rad2deg)

#=================================================================================

def genUser():
	'''
	To generate a random user from randomuser.me
	:return: Wingo User
	'''
	data = requests.get("http://api.randomuser.me/0.5/")
	data = data.json()["results"][0]["user"]

	user          = User()
	user.email    = data["email"]
	user.password = data["md5"]
	user.name 	  = data["username"]
	user.avatar   = data["picture"]["thumbnail"]


	return user

#=================================================================================

def genNote(author, latitude=48.4000000 , longitude= -4.4833300, max_distance = 5000):
	'''
	To generate a random note from position 
	:return: Wingo Note 
	'''	
	note           = Note()
	note.location  = computeNewPointFrom(latitude, longitude, randint(0,359), randint(0,max_distance))
	note.message   = genText()
	note.author    = author

	return note

#=================================================================================

def genComment(author, message = None):
	'''
	To generate a random comment for author 
	:return: Wingo Comment 
	'''	
	comment = Comment()
	if message is None:
		comment.message = genText(30)
	else :
		comment.message  = message 
	comment.author = author 

	return comment 

#=================================================================================

def genAll(latitude, longitude, radius, noteCount, userCount, verbose = False):
	'''
	To generate a database 
	'''	
	print("generate ")
	dropAll()

	admin = User();
	admin.email    = "dridk@dridk.fr"
	admin.password = "dridk"
	admin.name 	   = "dridk"
	admin.avatar   = "https://secure.gravatar.com/avatar/3d109adaffa634df6f23fc08447244a5?s=200&d=identicon"
	admin.save()

	

	for i in range(userCount):
		user = genUser()
		user.save()
		print("create user " + user.name + " ...")

	print("creating notes ...")
	for j in range(noteCount):
		note = genNote(user,latitude=latitude , longitude= longitude, max_distance = radius)
		note.save()

		for c in range(randint(0, 5)):
			comment = genComment(user)
			note.comments.append(comment)
			note.save()







