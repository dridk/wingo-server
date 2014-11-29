import requests 
import json 
import unittest
from mongoengine import *
from mongoengine.connection import disconnect
import application as mainApp
from models import *
from test.util import *

current_location = ["49.17970","-0.36960"]

class NoteViewTest(unittest.TestCase):


	def setUp(self):
		disconnect()
		connect("wingoTest")
		self.app  = mainApp.app.test_client()	
		generate_data()
		

	def test_get_one_note(self):
		uri = "/notes/{}".format(str(Note.objects.first().id))
		data = self.app.get(uri).data
		print_json(data)
		print (Note.objects.first().id)
		
	

	def test_get_notes_radius_150(self):
		uri = '/notes?lat='+current_location[0]+'&lon='+current_location[1]+'&radius=150'
		data = self.app.get(uri).data.decode("utf-8")
		print_json(data)
		array = check_json(data)
		# self.assertEqual(len(array["results"]), 1, "Two many place are found. Only library should be there")

	def test_get_notes_radius_500(self):
		uri = '/notes?lat='+current_location[0]+'&lon='+current_location[1]+'&radius=500'
		data = self.app.get(uri).data.decode("utf-8")
		print_json(data)
		array = check_json(data)
		# self.assertEqual(len(array["results"]), 1, "Two many place are found. Only library should be there")

	def test_get_notes_radius_1000(self):
		uri = '/notes?lat='+current_location[0]+'&lon='+current_location[1]+'&radius=10000'
		data = self.app.get(uri).data.decode("utf-8")
		print_json(data)
		array = check_json(data)

	def test_get_tags(self):
		uri = '/tags?lat='+current_location[0]+'&lon='+current_location[1]+'&radius=1000'
		data = self.app.get(uri).data.decode("utf-8")
		print_json(data)
		array = check_json(data)



	def test_post_notes(self):
		data = self.app.get('/notes').data.decode("utf-8")
		headers = {'content-type': 'application/json'}
		payload = {"author":"darwin", "message":"this is a test", "lat":43.82186,"lon":-79.42456}
		data =self.app.post("/notes",headers=headers,data=json.dumps(payload)).data.decode("utf-8")
		print_json(data)
		array = check_json(data)
		check_success(array) 
	


        
	def tearDown(self):
		pass
		# db = connect('wingoTest')
		# db.drop_database('wingoTest')



if __name__ == '__main__':
	unittest.main()