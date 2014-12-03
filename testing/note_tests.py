import sys, os.path
#ADD PARENT FOLDER 


import os
import unittest
import requests 
import json 
from mongoengine.connection import disconnect

from wingo.application import app
from wingo.models import *

from testing.util import *
class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
    	connect("wingo")
    	self.app = app.test_client()

    def tearDown(self):
    	pass


    def test_get_one_note(self):
    	uri = "/notes/{}".format(str(Note.objects.first().id))
    	data = self.app.get(uri).data
    	print_json(data)
    	print(Note.objects.first().id)



if __name__ == '__main__':
    unittest.main()