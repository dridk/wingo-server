from datetime import datetime
from mongoengine import *
from bson.objectid import ObjectId
import config

class PocketNote(EmbeddedDocument):
	author     = ReferenceField("User", required=True)
	message    = StringField(required = True, max_length=config.MAX_NOTE_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.now, required=True)
	location   = PointField()

	@staticmethod
	def from_note(note):
		if isinstance(note,eval("Note")):
			pocket = PocketNote()
			pocket.author    = note.author
			pocket.message   = note.message
			pocket.picture   = note.picture
			pocket.timestamp = note.timestamp
			pocket.location  = note.location
			return pocket
		return None
 

class User(Document):
	email    = EmailField(required=True)
	password = StringField(required=True)
	nickname = StringField(required=True)
	avatar   = URLField()
	pockets  = ListField(EmbeddedDocumentField(PocketNote))

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
	takes      = IntField(default=0)
	limit      = IntField(default=-1)
	tags       = ListField(StringField())
	comments   = ListField(EmbeddedDocumentField(Comment))
	


	


	def __str__(self):
		return str(self.message)

	def clean(self):
		#Extract tags when saving notes
		self.tags = [i for i in self.message.split(" ") if i.startswith("#")]
