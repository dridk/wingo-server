from datetime import datetime
from mongoengine import *
from bson.objectid import ObjectId
from itsdangerous import Signer
import wingo.config as config


class PocketNote(EmbeddedDocument):
	author     = ReferenceField("User", required=True)
	message    = StringField(required = True, max_length=config.MAX_NOTE_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.utcnow, required=True)
	location   = PointField()
	parent     = ObjectIdField(required=True)
	signature  = StringField(required=True)

	@staticmethod
	def from_note(note):
		if isinstance(note,eval("Note")):
			pocket = PocketNote()
			pocket.author    = note.author
			pocket.message   = note.message
			pocket.picture   = note.picture
			pocket.timestamp = note.timestamp
			pocket.location  = note.location
			pocket.parent    = note.id

			key = str(note.id)
			s = Signer(config.SECRET_KEY)
			signing = str(s.sign(bytes(key, "utf-8")))
			pocket.signature = signing
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

	def has_note(self, note):
		if isinstance(note,eval("Note")):
			for p in self.pockets:
				if p.parent == note.id:
					return True
		return False






	def __str__(self):
		return str(self.nickname)



class Comment(Document):
	author    = ReferenceField(User, required=True)
	message   = StringField()
	timestamp = DateTimeField(required=True,default=datetime.utcnow)


class Note(Document):
	author     = ReferenceField(User, required=True)
	anonymous  = BooleanField(required=True, default = True)
	message    = StringField(required = True, max_length=config.MAX_NOTE_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.utcnow, required=True)
	location   = PointField()
	expiration = DateTimeField()
	takes      = IntField(default=0)
	limit      = IntField(default=-1)
	tags       = ListField(StringField())
	comments   = ListField(ReferenceField(Comment))
	


	


	def __str__(self):
		return str(self.message)

	def clean(self):
		#Extract tags when saving notes
		self.tags = [i for i in self.message.split(" ") if i.startswith("#")]
