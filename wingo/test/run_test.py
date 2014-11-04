import unittest
import requests 
import json 
from test.note_test import *


#TYPE pyrg run_test.py -v
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARN = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

class TuLogManager():
	""" HElper to manage/display beautifull consol log/print """

	def printSectionProgress(sectionName, currentStep, totalStep, success):
		sys.stdout.write("   > {0:20}: {1:3}/{2:3}    " )
		sys.stdout.flush()




if __name__ == '__main__':
	unittest.main()

