import unittest 
from wingo import create_app 
from wingo.models import *
from dbtools.utils import *
import os
import json 


def check_json(data):
	results = json.loads(data)
	if "success" not in data:
		raise Warning("Wingo json schema is wrong. success is mandatory")
	return results

def check_success(obj):
	if obj["success"] is False:
		raise Warning(obj["message"])




class TestAPI(unittest.TestCase):

	def setUp(self):
		print("test begin")
		self.app = create_app(os.environ.get("WINGO_CONFIG","testing")).test_client()

		if Note.objects.count() == 0:
			genAll(48.386537, -4.490095, 5000, 10, 5)


	def tearDown(self):
		print("test end")


	def test_user(self):
		uri = "/api/v1/users"
		data = self.app.get(uri).data.decode("utf-8") 
		print(data)
		results = check_json(data)
		check_success(results)