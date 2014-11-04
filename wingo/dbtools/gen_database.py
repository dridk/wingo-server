#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import argparse
import requests 
import json 
import sys 
import mongoengine as mongo


from ..models import *
from gen_utils import *




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Arguments definition 													    #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
parser = argparse.ArgumentParser(description="Wingo database generation tool.\n")


parser.add_argument('-tpl', dest='tplFile', type=str, choices=['Toulouse', 'Brest', 'Toronto', 'Caen', 'France', 'World'], nargs='+', default=None,
                   help="load one or more template file and generate data according it.")


parser.add_argument('-f', '--find', dest='searchLocation', type=str, default=None,
                   help='try to find a location and generate notes around it.')

parser.add_argument('-p', '--position', dest='position', type=float, nargs=2, default=None,
                   help='the position : latitude and longitude.')


parser.add_argument('-r', '--radius', dest='radius', type=float, default=1,
                   help='radius in kilometers used for the generation around a point.')

parser.add_argument('-c', '--count', dest='count', type=int, default=100,
                   help='the number of note that will be generated. Default is 100.')


parser.add_argument('-db', dest='database', type=str, default='wingo',
                   help="the database name to use. Default is 'wingo'.")

parser.add_argument('-nd', '--NODROP', dest='dropDB', action='store_false', default=True,
                   help="don't drop the database before doing the generation. New data will be added to the old ones.")


parser.add_argument('-s', '--silent', dest='verbose', action='store_false', default=True,
                   help="silent mode : no message displayed.")












# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MAIN GENERATION SCRIPT 													#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

args = parser.parse_args()


#Set verbose mode :
dbToolVerboseMode = args.verbose


msg("Connect to database")
try:
	connect(args.database) 
except Exception, e:
	error("Unable to connect to database '" + args.database +"'", e)
	sys.exit(100) # DB error


# Check if need to drop the database 
if args.dropDB:
	msg("Database " + y("dropped"))
	try:
		Note.drop_collection()
		User.drop_collection()
	except Exception, e:
		error("Drop collection failled", e)
		sys.exit(110) # DB drop error
else:
	msg("Database not dropped")


# Using template
if args.tplFile is not None:
	msg("Template file used for the generation " + lst2str(args.tplFile))
	

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