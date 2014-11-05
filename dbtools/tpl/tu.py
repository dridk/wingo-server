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


currentTime  = datetime.utcnow()
users 		 = ['sacha', 'olivier', 'eugene']

# all lists below must have same count of values. For each location, point will
# be generated according to values in these lists

authors      = [ 0,  1,   2,   0,    1]
anonymous    = [ 0,  0,   0,   1,    1]
radius       = [10, 50, 100, 500, 1000]  # in meters
dateDelta	 = [ 0, 10,  10,  10,   10]  # in minutes
limits		 = [-1, 10,  -1,   5,    5]  # -1 = no limit
taken		 = [ 1,  2,   3,   4,    5]  # 
commByNote   = [ 0,  1,  10,  50,    0] 
tagsByNote   = ["#dog", "#red", "#car", "#dog #car", ""]




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Static DATA															 	#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

locations = [
# Fake point
	["A", 	 45.0,  45.0],
	["B", 	 45.0, -45.0],
	["C", 	-45.0,  45.0],
	["D", 	-45.0, -45.0],
	["0",	  0.0,   0.0]
# Real points
#	["Eiffel tower",	48.858355,  2.294467],
#	["Caen's Phenix",	49.189183, -0.363914]
]






# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# GENERATION SCRIPT														 	#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

def genData():
	msg("-------------------------------------------------------")
	msg("UNIT TESTS database generation")

	# ---------------------------------------------------------------------------
	head("USERS generation :" )
	authorsList = []
	for i in range(0, len(users)):
		usr = users[i]
		authorsList.append(
			User(email=usr+"@labsquare.org",
				password="pass",
				nickname=usr))
		authorsList[i].save()
		msg("   > " + y(usr) + " genereted")

	msg("   >> total " + r(len(users))  + " users have been generated")



	# ---------------------------------------------------------------------------
	head("NOTES generation :" )

	for loc in locations:

		# generate notes arround the location
		for i in range(0, len(authors)):

			note = Note()
			note.anonymous = bool(anonymous[i])
			note.author = authorsList[authors[i]]
			note.message = loc[0] + " : " + str(radius[i]) + "m by " + users[authors[i]] + " " + tagsByNote[i]
			note.location = computeNewPointFrom(loc[1], loc[2], randint(0,359), radius[i])
			note.takes = taken[i]
			note.limit = limits[i]
			note.timestamp = currentTime - timedelta(0, 0, 0, 0, dateDelta[i])

			# Generate comments
			if commByNote[i] > 0:
				note.comments = []
				date = note.timestamp
				for j in range(0, commByNote[i]):
					comment = Comment()
					comment.author = authorsList[authors[i % len(authors)]]
					comment.date = date + timedelta(0, 0, 0, 0, j+1) # add comment each minute
					comment.message = genText("Comment n°" + str(j+1) + " for the note \"" + note.message + "\"")
					note.comments.append(comment)

			note.save()

		msg("   > {0:5} ".format(loc[0] + " :") + y(len(authors)) + " notes generated arround (" + str(loc[1]) + ", " + str(loc[2]) + ")")
	msg("   >> total " + r(len(locations) * len(authors))  + " notes have been generated           ")
	msg("")