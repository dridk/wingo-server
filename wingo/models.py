from mongoengine import * 
from datetime import datetime
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


	def __str__(self):
		return self.name


#=======================================================================

class Comment(EmbeddedDocument):
	author    = ReferenceField(User, required=True)
	message   = StringField()
	timestamp = DateTimeField(required=True,default=datetime.now)

	def export_data(self):
		return {
		"message"     : self.message,
		"name "       : self.author.name,
		"avatar"      : self.author.avatar,
		"timestamp"   : self.timestamp
		}

#=======================================================================

class Note(Document):
	author      = ReferenceField(User, required=True)
	location    = GeoPointField(required=True)
	message     = StringField(required=True)
	media       = URLField()
	timestamp   = DateTimeField(default=datetime.now, required=True)
	expiration  = DateTimeField()
	takes       = IntField(default=0, required=True)
	takes_limit = IntField()
	tags        = ListField(StringField())
	comments    = ListField(EmbeddedDocumentField(Comment))

	def export_data(self):
		res =  {
			"author.name"      	: self.author.name,
			"author.avatar"    	: self.author.avatar,
			"lon"			   	: self.longitude() ,
			"lat" 				: self.latitude(),
			"message"			: self.message,
			"media"				: self.media ,
			"timestamp"			: self.timestamp ,
			"takes"				: self.takes,
			"comment_count"     : len(self.comments),
			"tags"				: self.tags,
			"has_max_takes"		: False,
			"has_expiration"	: False
 		}

		if self.takes_limit is not None:
 			res["has_max_takes"] = True 
 			res["max_takes"]    = self.takes_limit

		if self.expiration is not None:
 			res["has_expiration"] = True 
 			res["expiration"]      = self.takes_limit

		return res

	''' Extract tags when saving note. This is a parent methods '''
	def clean(self):
		self.tags = [i for i in self.message.split(" ") if i.startswith("#")]

	def import_data(self, data):
		pass

	@property
	def latitude(self):
		return float(self.location[0])

	@property
	def longitude(self):
		return float(self.location[1])

	@latitude.setter
	def latitude(self, v):
		self.location[0] = v 

	@longitude.setter
	def longitude(self, v):
		self.location[1] = v 




	def __str__(self):
		return self.message[:10] + "..."

