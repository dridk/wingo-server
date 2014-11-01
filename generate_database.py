#!/usr/bin/env python
# -*- coding: utf-8 -*-

from loremipsum import *
import math
from datetime import *
from random import randint
from wingo.models import *
import json
import requests


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# TOOLS                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# http://www.movable-type.co.uk/scripts/latlong.html

# Color in shell
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# To generate 255 txt.
def genText(maxLen):
	txt = get_paragraph()
	if len(txt)>maxLen:
		return txt[0:maxLen]
	else:
		return txt



# To generate a new position from a start position, an angle and a distance (lat/lon, degree, meter)
def computeNewPointFrom(lat1, lon1, bearing, distance):
	#constants
	dR = (distance / 1000.0) / 6373.0
	deg2rad = math.pi/180.0

	# convert angle in radian
	lat1 = lat1 * deg2rad
	lon1 = lon1 * deg2rad
	brng = bearing * deg2rad

	lat2 = math.asin( math.sin(lat1) * math.cos(dR) + math.cos(lat1) * math.sin(dR) * math.cos(brng) )
	lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(dR) * math.cos(lat1), math.cos(dR) - math.sin(lat1) * math.sin(lat2))

	# convert back to degree
	rad2deg = 180.0 / math.pi
	return [lat2 * rad2deg, lon2 * rad2deg]


# To generate X point in an area define by a center position and a radius (in meter)
def genPackedPosition(lat, lon, radius, nbr):
	return [computeNewPointFrom(lat, lon, randint(0,359), randint(0,radius)) for i in range(0, nbr)]


def genTags(nbr, tags):
	result = ""
	for i in range(0, nbr):
		result += " #" + tags[randint(0, len(tags) -1)]
	return result


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Static DATA                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# gg maps or http://universimmedia.pagesperso-orange.fr/geo/loc.htm
locations = [
#Toulouse
	["Ikit Home", 		43.602574, 1.409293],
	["Place Wilson", 	43.604858, 1.447401],
	["Sopra Office", 	43.612457, 1.306566],
	["La Daurade", 		43.601337, 1.438675],
#Nante
	["La Massoniere",	47.145684, -1.310307],
	["Gare de Nantes",	47.217507, -1.542068],
#Renne
	["Dinge",			48.357953, -1.712657],
	["Concert", 		48.149191, -1.685786],
	["Gare de Rennes",	48.103361, -1.672540],
#Brest
	["Sacha Home",		48.386537, -4.490095],
	["CHU Brest",		48.401642, -4.527679],
	["Parc St Pierre",	48.400850, -4.522467],
#Caen
	["Mairie",			49.181076, -0.370995],
	["Chateau",			49.186462, -0.362562],
	["Phenix",			49.189183, -0.363914],
	["Saint Pierre",	49.183724, -0.361124],
	["Gueudelot House",	49.237472, -0.412254],
	["Gare de Caen",	49.175949, -0.348888],
#Toronto 
	["Eugene Home",		43.821846, -79.424579],
	["City Hall Lib",	43.652414, -79.381567],
	["Queen's Park",	43.661930, -79.391481]
]


tags = [
	"dog", "cat", "food", "fresh", "tasty", "mug", "drink", "coffeeaddict", "coffee", "cafe", "pattern", "onedirection", "harrystyles", "niallhoran",
	"love", "TagsForLikes", "tweegram", "photooftheday", "20likes", "amazing", "smile", "look", "igers", "picoftheday", "hot", "instadaily", "instafollow",
	"followme", "girl", "iphoneonly", "instagood", "bestoftheday", "instacool", "instago", "all_shots", "follow", "webstagram", "colorful", "style", "swag",
	"nature", "sky", "sun", "beautiful", "sunrise", "flowers", "night", "tree", "twilight", "clouds", "cloudporn", "dusk", "mothernature", "geometric",
	"artwork", "architecture", "building", "city", "skyscraper", "urban", "design", "minimal", "town", "art", "lookingup", "composition", "geometry", "perspective",
	"zaynmalik", "louistomlinson", "liampayne", "katyperry", "bieberfever", "justinb", "justindb", "forever"
	]









# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# GENERATION                                                                #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
dbName       = 'wingo'
userMax      = 40        # to get more (max 200) need dev account with key - using randomuser.me website api
dateDelta    = 7*24*60   # in minutes
radiusByArea = 500.0     # in meters
notesByArea  = [15, 30]  # min and max notes by area
commByNote   = [1, 15]   # min and max comments by notes (~ 50% of notes will have comments)


connect(dbName) 
print("Regenaration of the database '"+ dbName +"'")
currentTime = datetime.utcnow()

# ---------------------------------------------------------------------------
print(bcolors.HEADER +" - USERS generation :" + bcolors.ENDC)
User.drop_collection()

data = requests.get("http://api.randomuser.me/?results=" + str(userMax))
data = data.json()["results"]
for i in range(0, userMax):
	usr = data[i]["user"]
	User(email=usr["email"],
		password=usr["md5"],
		nickname=usr["username"]).save()
		# avatar=usr["thumbnail"]

print("   >> " + bcolors.FAIL + str(userMax) + bcolors.ENDC + " users created")



# ---------------------------------------------------------------------------
print(bcolors.HEADER +" - NOTES generation :" + bcolors.ENDC)
Note.drop_collection()
totalNotesCount = 0
for loc in locations:
	noteCount = randint(notesByArea[0], notesByArea[1])
	totalNotesCount += noteCount + 1
	notePositions = genPackedPosition(loc[1], loc[2], radiusByArea, noteCount)

	# create the "central" note for the area
	note = Note()
	note.author = User.objects[0]
	note.message = loc[0] 
	note.location= [loc[1], loc[2]]
	note.save()

	# generate notes arround
	for nP in notePositions:
		note = Note()
		note.anonymous = randint(0,2) != 0
		note.author = User.objects[randint(0,userMax-1)]
		note.message = loc[0] + " : " + genText(120) + genTags(randint(1,3), tags)
		note.location=nP
		note.takes = randint(0,300)
		note.timestamp = currentTime - timedelta(0, 0, 0, 0, randint(0, dateDelta))
		note.save()

	msg = "   > {0:20} ".format(loc[0] + " :") + bcolors.WARN + str(noteCount + 1) + bcolors.ENDC + " notes generated arround"
	print(msg)

print("   >> total " + bcolors.FAIL + str(totalNotesCount) + bcolors.ENDC + " notes have been generated ")




# ---------------------------------------------------------------------------
# Comments


