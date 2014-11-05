from datetime import datetime
from mongoengine import *
import config


 

class User(Document):
	email    = EmailField(required=True)
	password = StringField(required=True)
	nickname = StringField(required=True)
	avatar   = URLField()
	pockets  = ListField(IntField)

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
	location   = PointField(required=True)
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
