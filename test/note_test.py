import unittest
import requests 
import json 
import mim

class DashViewTest(unittest.TestCase):
	def setUp(self):
		mim.app.config['TESTING'] = True
		self.app = mim.app.test_client()
		user = mim.models.User(email="testing@labsquare.org", password="", username="testing")
		user.save()
		for i in range(5):
		    dashview = mim.models.DashView()
		    dashview.owner = user 
		    dashview.title = "test"
		    dashview.description = "test"
		    dashview.save()
        

	def tearDown(self):
		mim.models.User.objects.filter(username="testing").delete()
		mim.models.DashView.objects.filter(title__contains="test").delete()

	def check_json_error(self,data):
		if "message" in data:
			raise Warning("JSON message : " + data["message"])

	def is_dashview(self,data):
		self.assertIn("id",data)
		self.assertIn("created",data)
		self.assertIn("title",data)
		self.assertIn("description",data)
		self.assertIn("owner",data)
		
	def get_dashview_id(self):
		return str(mim.models.DashView.objects.filter(title="test").first().id)


	def test_get_dashview_list(self):
		data = self.app.get("/api/dashviews").data 
		array = json.loads(data)
		self.assertIn("results",array)
		for view in array["results"]:
			self.is_dashview(view)

	def test_get_dashview(self):
		view_id = self.get_dashview_id()
		data = self.app.get("/api/dashviews/" + view_id).data 
		array = json.loads(data)
		self.is_dashview(array["results"])

	def test_delete_dashview(self):
		view_id = self.get_dashview_id()
		data =self.app.delete("api/dashviews/" + view_id).data
		array = json.loads(data)
		self.assertIn("success",array)

	def test_post_dashview(self):
		firstUserId = str(mim.models.User.objects.first().id)
		payload = {"title":"testPosted", "description":"descriptionPosted", "owner":firstUserId}
		headers = {'content-type': 'application/json'}
		data =self.app.post("/api/dashviews", headers=headers, data=json.dumps(payload)).data 
		array = json.loads(data)
		self.check_json_error(array)
		self.assertIn("success",array)
		self.assertTrue(array["success"], "success equal false")
		self.assertIn("id",array["results"])

	def test_put_dashview(self):
		payload = {"title":"testPosted", "description":"descriptionPosted"}
		headers = {'content-type': 'application/json'}
		dashview_id = self.get_dashview_id()
		data =self.app.put("/api/dashviews/" +dashview_id, 
							 data = json.dumps(payload),
							 headers = headers).data

		array = json.loads(data)
		self.check_json_error(array)

		updatedDashview = mim.models.DashView.objects.get(pk=dashview_id)
		self.assertEqual(payload["title"], updatedDashview.title)
		self.assertEqual(payload["description"], updatedDashview.description)
