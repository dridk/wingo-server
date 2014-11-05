#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import argparse
import requests 
import json 
import sys 
import mongoengine as mongo


from wingo.models import *
from dbtools import *
from dbtools.utils import * # to be able to use directly msg(), err(), ...
from dbtools.tpl import *




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Arguments definition 													    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
parser = argparse.ArgumentParser(description="Wingo database generation tool.\n")


parser.add_argument('-tpl', dest='tplFiles', type=str, choices=['XuFu', 'TU', 'Cities3', 'France', 'World'], nargs='+', default=None,
                   help="load one or more template file and generate data according it.")


parser.add_argument('-f', '--find', dest='searchLocation', type=str, default=None,
                   help='try to find a location and generate notes around it.')

parser.add_argument('-p', '--position', dest='position', type=float, nargs=2, default=None,
                   help='the position : latitude and longitude.')


parser.add_argument('-r', '--radius', dest='radius', type=float, default=1,
                   help='radius in kilometers used for the generation around a point.')

parser.add_argument('-c', '--count', dest='count', type=int, default=100,
                   help='the number of note that will be generated. Default is 100.')


parser.add_argument('-db', dest='database', type=str, default='wingo_test',
                   help="the database name to use. Default is 'wingo_test'.")

parser.add_argument('-d', '--DROP', dest='dropDB', action='store_true', default=False,
                   help="drop the database before doing the generation.")


parser.add_argument('-s', '--silent', dest='verbose', action='store_false', default=True,
                   help="silent mode : no message displayed.")












# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MAIN GENERATION SCRIPT 													#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

args = parser.parse_args()


#Set verbose mode :
dbToolVerboseMode = args.verbose


msg("Connect to database '" + r(args.database) + "'")
try:
	connect(args.database) 
except Exception, e:
	error("Unable to connect to database '" + args.database +"'", e)
	sys.exit(100) # DB error


# Check if need to drop the database 
if args.dropDB:
	msg("Database dropped. Old data will be " + r("erased") + ".")
	try:
		Note.drop_collection()
		User.drop_collection()
	except Exception, e:
		error("Drop collection failled", e)
		sys.exit(110) # DB drop error
else:
	msg("Database not dropped. Data will be " + r("merged") + ".")


# Using template
if args.tplFiles is not None:
	msg("Template file used for the generation " + lst2str(args.tplFiles))
	
	for tpl in args.tplFiles:
		if tpl == 'XuFu':
			xufu.genData()
		elif tpl == 'TU':
			tu.genData()


else:
	# using search or location ?
	if args.searchLocation is not None:
		msg("Try to find location from search string : " + args.searchLocation)
	elif args.position is not None:
		msg("Generate data around location : (" + str(args.position[0]) + ", " + str(args.position[1]) + ")")
	else:
		error("No location defined for the generation.")
		sys.exit(404)


# Exit script without error
sys.exit(0) 