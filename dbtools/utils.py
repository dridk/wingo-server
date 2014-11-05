
import sys 
import math


from loremipsum import *
from random import randint



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# LOG TOOLS			 													    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


dbToolVerboseMode = True


# color in shell
class bC:
	H = '\033[95m' # Header 	(purple)
	O = '\033[92m' # Ok 		(green)
	W = '\033[93m' # Warning 	(Yellow)
	F = '\033[91m' # Fail 		(Red)
	E = '\033[0m'  # -end


# Print messages
def msg(message):
	if dbToolVerboseMode:
		print message

def error(message, exception=None):
	if dbToolVerboseMode:
		print bC.F + "Error : " + bC.E + message
		if exception is not None:
			print bC.F + "Exception : " + bC.E + exception.message

def warn(message):
	if dbToolVerboseMode:
		print bC.W + "Warning : " + bC.E + message


def head(message):
	if dbToolVerboseMode:
		print bC.H + " - " + message + bC.E

def g(message):
	return bC.O + str(message) + bC.E
def y(message):
	return bC.W + str(message) + bC.E
def r(message):
	return bC.F + str(message) + bC.E

def lst2str(theList):
		return '{' + ', '.join(theList) + '}'


def  progress(msg):
	sys.stdout.write(msg + "\r")
	sys.stdout.flush()




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# TEXT TOOLS			 												    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# To generate 255 txt.
def genText(maxLen):
	txt = get_paragraph()
	if len(txt)>maxLen:
		return txt[0:maxLen]
	else:
		return txt



def genTags(nbr, tags):
	result = ""
	for i in range(0, nbr):
		result += " #" + tags[randint(0, len(tags) -1)]
	return result







# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# GEOPOINT TOOLS		 												    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


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

