from datetime import datetime
from mongoengine import *
import config


class Cache(EmbeddedDocument):
	location  = PointField(required=True)
	radius    = IntField(required=True)
	filters   = StringField(required = True)
	date      = DateTimeField(required=True)
	cachePath = StringField(required=True)

class Device(EmbeddedDocument):
	uid   = UUIDField(required=True)
	name  = StringField()
	cache = Cache()




class User(Document):
	email    = EmailField(required=True)
	password = StringField(required=True)
	nickname = StringField(required=True)
	avatar   = URLField()
	pockets  = ListField(IntField)
	devices  = ListField(Device)


	def __str__(self):
		return str(self.nickname)

class Note(Document):
	author     = ReferenceField(User, required=True)
	anonymous  = BooleanField(required=True, default = True)
	message    = StringField(required = True, max_length=config.MAX_NOTE_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.now, required=True)
	location   = PointField(required=True, auto_index=True)
	expiration = DateTimeField()
	takes      = IntField()
	limit      = IntField(default=-1)
	tags       = ListField(StringField())
	def __str__(self):
		return str(self.timestamp)

	def clean(self):
		#Extract tags when saving notes
		self.tags = [i for i in self.message.split(" ") if i.startswith("#")]


class Comment(Document):
	author  = ReferenceField(User, required=True)
	note    = ReferenceField(Note, required=True)
	comment = StringField()

