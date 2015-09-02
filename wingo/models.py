from mongoengine import * 
from datetime import datetime
from bson.objectid import ObjectId
from wingo.exceptions import CustomError
from flask import url_for



#=======================================================================

class User(Document):
	""" User Model Object """ 
	email        = EmailField(required =True)
	password     = StringField(required=True)
	name         = StringField(required=True)
	avatar       = URLField()
	verified     = BooleanField(default=False , required=True)
	pocket_notes = ListField(ReferenceField("Note"))
	notes        = ListField(ReferenceField("Note"))

	def export_data(self):
		return {
			"id"	       : str(self.id),
			"name"         : self.name,
			"email"        : self.email,
			"avatar"       : self.avatar,
			"verified"     : self.verified,
			"note_count"   : len(self.notes),
			"pocket_count" : len(self.pocket_notes),
			"uri"	       : url_for('api.get_user', id=self.id, _external=True)
 		}

	def import_data(self, data):
		self.name     = data["name"]
		self.email    = data["email"]
		self.password = data["password"]
		self.avatar   = data["avatar"]


	@staticmethod
	def from_id(user_id):
		if not ObjectId.is_valid(user_id):
			return None;
		
		user = User.objects.get(pk=user_id)
		return user
	

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

	def import_data(self, data):
		try:
			self.message     = data.get("message")
			self.author      = User.objects.first() # Current user replace
		except KeyError as e: 
			raise CustomError("Invalid Comment: missing " + e.args[0])


	def __str__(self):
		return self.message

#=======================================================================

class Note(Document):
	author      = ReferenceField(User, required=True)
	location    = PointField(required=True, auto_index=False)
	message     = StringField(required=True)
	media       = URLField()
	timestamp   = DateTimeField(default=datetime.now, required=True)
	expiration  = DateTimeField()
	takes       = IntField(default=0, required=True)
	takes_limit = IntField()
	tags        = ListField(StringField())
	comments    = ListField(EmbeddedDocumentField(Comment))
	die         = BooleanField(required=True , default=False)


	meta = {
        'indexes': [[("location", "2dsphere"), ("timestamp", 1), ("takes",1)]]
        # 'ordering' : ['timestamp']
    }

	def export_data(self):
		res =  {
			"id"	   			: str(self.id),
			"author.name"      	: self.author.name,
			"author.avatar"    	: self.author.avatar,
			"lon"			   	: self.longitude ,
			"lat" 				: self.latitude,
			"message"			: self.message,
			"media"				: self.media ,
			"timestamp"			: self.timestamp ,
			"takes"				: self.takes,
			"comment_count"     : len(self.comments),
			"tags"				: self.tags,
			"has_max_takes"		: False,
			"has_expiration"	: False, 
			"die"               : self.die,
			"uri"	            : url_for('api.get_note', id=self.id, _external=True)

 		}

		if self.takes_limit is not None:
 			res["has_max_takes"] = True 
 			res["max_takes"]    = self.takes_limit

		if self.expiration is not None:
 			res["has_expiration"] = True 
 			res["expiration"]     = self.takes_limit

		return res

	''' Extract tags when saving note. This is a parent methods '''
	def clean(self):
		self.tags = [i for i in self.message.split(" ") if i.startswith("#")]

	def import_data(self, data):
		pass

	@property
	def latitude(self):
		if isinstance(self.location, dict):
			return float(self.location["coordinates"][0])
		else:
			return float(self.location[0])

	@property
	def longitude(self):
		if isinstance(self.location, dict):
			return float(self.location["coordinates"][1])
		else:
			return float(self.location[1])

	@latitude.setter
	def latitude(self, v):
		if isinstance(self.location, dict):
			self.location["coordinates"][0] = v
		else:
			self.location[0] = v 

	@longitude.setter
	def longitude(self, v):
		if isinstance(self.location, dict):
			self.location["coordinates"][1] = v
		else:
			self.location[1] = v 




	def __str__(self):
		return self.message[:10] + "..."

