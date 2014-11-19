from datetime import datetime
from mongoengine import *
from bson.objectid import ObjectId
import config

class UserNote(EmbeddedDocument):
	author     = ReferenceField("User", required=True)
	message    = StringField(required = True, max_length=config.MAX_NOTE_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.now, required=True)
	location   = PointField()

	def from_notes(self,note):
		if isinstance(note,eval("Note")):
			self.author    = note.author
			self.message   = note.message
			self.picture   = note.picture
			self.timestamp = note.timestamp
			self.location  = note.location
 

class User(Document):
	email    = EmailField(required=True)
	password = StringField(required=True)
	nickname = StringField(required=True)
	avatar   = URLField()
	pockets  = ListField(EmbeddedDocumentField(UserNote))

	@staticmethod
	def from_id(user_id):
		if not ObjectId.is_valid(user_id):
			return None;
		
		user = User.objects(pk=user_id).first()
		return user


	def __str__(self):
		return str(self.nickname)



class Comment(EmbeddedDocument):
	author    = ReferenceField(User, required=True)
	message   = StringField()
	timestamp = DateTimeField(required=True,default=datetime.now)


class Note(Document):
	author     = ReferenceField(User, required=True)
	anonymous  = BooleanField(required=True, default = True)
	message    = StringField(required = True, max_length=config.MAX_NOTE_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.now, required=True)
	location   = PointField()
	expiration = DateTimeField()
	takes      = IntField()
	limit      = IntField(default=-1)
	tags       = ListField(StringField())
	comments   = ListField(EmbeddedDocumentField(Comment))
	

	


	def __str__(self):
		return str(self.message)

	def clean(self):
		#Extract tags when saving notes
		self.tags = [i for i in self.message.split(" ") if i.startswith("#")]
