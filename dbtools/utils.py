from loremipsum import *
import math
from datetime import *
from random import randint
import requests
from wingo.models import *

_TAGS = []
_LOCATION = []

'''To generate 255 txt 

:param maxLen: the length of message 
:return: random text
'''
def genText(maxLen=100):
	return get_paragraph()[:maxLen]


def genTags(count=4):
	global _TAGS
	if not _TAGS :
		with open("dbtools/tags.txt","r") as file :
			_TAGS = file.read().splitlines()

			return '#'+' #'.join(_TAGS[:count])



'''To generate a new position from a start position, an angle and a distance (lat/lon, degree, meter)

:param lat: latitude of the center
:param lon: longitude of the center 
:param bearing: direction from the center
:param distance: distance from the centr
:return: a tuple (latitude, longitude)
'''
def computeNewPointFrom(lat, lon, bearing, distance):
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

'''To generate a random user from randomuser.me
:return: Wingo User
'''
def genUser():
	data = requests.get("http://api.randomuser.me")
	data = data.json()["results"][0]["user"]

	user          = User()
	user.email    = data["email"]
	user.password = data["md5"]
	user.nickname = data["username"]
	user.avatar   = data["picture"]["thumbnail"]

	user.save()

	return user





