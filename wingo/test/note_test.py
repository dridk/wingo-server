import unittest
import requests 
import json 

from mongoengine import connect

from app import app
from models import *
from test.util import *



class NoteViewTest(unittest.TestCase):
	def setUp(self):
		self.app  = app.test_client()


	def test_get_one_note(self):
		uri = "/notes/{}".format(str(Note.objects.first().id))
		data = self.app.get(uri).data
		print_json(data)
		print Note.objects.first().id

	

	def test_get_notes(self):
		pass
		uri = '/notes?lat=43.82186&lon=-79.42456'
		data = self.app.get(uri).data
		print_json(data)



	def test_post_notes(self):
		data = self.app.get('/notes').data
		headers = {'content-type': 'application/json'}
		payload = {"author":"darwin", "message":"this is a test", "lat":43.82186,"lon":-79.42456}
		data =self.app.post("/notes",headers=headers,data=json.dumps(payload)).data 
		print_json(data)
		array = check_json(data)
		check_success(array) 
		pass


        
		
        

