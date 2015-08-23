import unittest 
from wingo import create_app 

class TestAPI(unittest.TestCase):

	def setUp(self):
		print("test begin")
		self.app = create_app("").test_client()


	def tearDown(self):
		print("test end")


	def test_user(self):
		uri = "/api/v1/users/"
		data = self.app.get(uri).data 
		print(data)