import unittest
import requests 
import json 
from app import app
from mongoengine import connect
from test.util import *

class NoteViewTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		connect("wingoTest")

	def test_get_notes(self):
		data = self.app.get('/notes').data
		check_json(data)

	def test_post_notes(self):
		data = self.app.get('/notes').data
		headers = {'content-type': 'application/json'}
		payload = {"author":"darwin"}
		data =self.app.post("/notes",headers=headers,data=json.dumps(payload)).data 
		array = check_json(data)
		check_success(array)


		print "SALUT"
		


        
		
        

