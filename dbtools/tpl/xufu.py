#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import sys 

from datetime import *
from random import randint

from wingo.models import *
from dbtools import *
from dbtools.utils import * # to be able to use directly msg(), err(), ...






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# PARAMETERS															 	#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

userMax	  	 = 40		 # to get more (max 200) need dev account with key - using randomuser.me website api
dateDelta	 = 7*24*60   # in minutes
radiusByArea = 500.0	 # in meters
notesByArea  = [15, 30]  # min and max notes by area
commByNote   = [1, 15]   # min and max comments by notes (~ 50% of notes will have comments)
maxTaken	 = 300
currentTime = datetime.utcnow()





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Static DATA															 	#
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
# GENERATION SCRIPT														 	#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


def genData():
	msg("-------------------------------------------------------")
	msg("XuFu test database generation")

	# ---------------------------------------------------------------------------
	head("USERS generation :" )
	data = requests.get("http://api.randomuser.me/?results=" + str(userMax))
	data = data.json()["results"]

	for i in range(0, userMax):
		usr = data[i]["user"]
		User(email=usr["email"],
			password=usr["md5"],
			nickname=usr["username"],
			avatar=usr["picture"]["thumbnail"]).save()

		progress("   >> {0}/{1}".format(i, userMax))
	msg("   >> " + r(userMax) + " users created")


	# ---------------------------------------------------------------------------
	head("NOTES generation :" )
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
			# limit/take
			limit = -1 # no limit by default
			if randint(0,2) != 0:
				limit = randint(1,100) * 10

			mTaken = maxTaken;
			if limit > 0:
				mTaken = limit
			taken = randint(0,mTaken)

			note = Note()
			note.anonymous = randint(0,2) != 0
			note.author = User.objects[randint(0,userMax-1)]
			note.message = loc[0] + " : " + genText(120) + genTags(randint(1,3), tags)
			note.location=nP
			note.takes = taken
			note.limit = limit
			note.timestamp = currentTime - timedelta(0, 0, 0, 0, randint(0, dateDelta))
			note.save()

		msg("   > {0:20} ".format(loc[0] + " :") + y(noteCount + 1) + " notes generated arround")
	msg("   >> total " + r(totalNotesCount)  + " notes have been generated           ")


	# ---------------------------------------------------------------------------
	head("COMMENTS generation :")
	totalCommsCount = 0

	notes = Note.objects.all()
	idx = 0
	maxN = len(notes)
	for note in notes:
		idx+=1
		if randint(0, 1) == 1:

			maxCom = randint(1, 10)
			totalCommsCount += maxCom
			note.comments = []
			date = note.timestamp

			for i in range(0, maxCom):
				comment = Comment()
				comment.author = User.objects[randint(0,userMax-1)]
				comment.date = date + timedelta(0, 0, 0, 0, 1) # add comment each minute
				comment.message = genText(100)
				note.comments.append(comment)

				progress("   > parsing note {0:3}/{1:3} : {2} comments created ".format(idx,maxN,totalCommsCount))
			note.save()

	msg("   >> total " + r(totalCommsCount) + " comments have been generated                ")
	msg("")