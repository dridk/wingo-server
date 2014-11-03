import unittest
import requests 
import json 
from app import app

class NoteViewTest(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_config(self):
		rv = self.app.get('/config')
		print rv.data
		
        
		
        

