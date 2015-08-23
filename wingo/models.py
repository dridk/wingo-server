from mongoengine import * 
from bson.objectid import ObjectId
from wingo.exceptions import ValidationError


#=======================================================================

class User(Document):
	""" User Model Object """ 
	email    = EmailField(required =True)
	password = StringField(required=True)
	name     = StringField(required=True)
	avatar   = URLField()

	def export_data(self):
		return {
			"name"     : self.name,
			"email"    : self.email,
			"avatar"   : self.avatar
 		}

	def import_data(self, data):
		try:
			self.name     = data["name"]
			self.email    = data["email"]
			self.password = data["password"]
			self.avatar   = data["avatar"]
		except KeyError as e: 
			raise ValidationError("Invalid User: missing " + e.args[0])

#=======================================================================

class Note(Document):
	author = ReferenceField(User, required=True)
	location = PointField()
	message= StringField(required=True)


class Livre(Document):
	title	= StringField(required=True)
	pages	= IntField(required=True)