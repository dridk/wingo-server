from mongoengine import * 
from bson.objectid import ObjectId


class User(Document):
	email    = EmailField(required =True)
	password = StringField(required=True)
	name     = StringField(required=True)

	def export_data(self):
		return {
			"name"     : self.name ,
			"email"    : self.email
		}

	def import_data(self, data):
		self.name     = data["name"]
		self.email    = data["email"]
		self.password = data["password"]
		# except KeyError as e: 
		# 	raise



class Livre(Document):
	title	= StringField(required=True)
	pages	= IntField(required=True)