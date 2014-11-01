from datetime import datetime
from mongoengine import *

MSG_LENGTH = 255


class User(Document):
	email    = EmailField(required=True)
	password = StringField(required=True)
	nickname = StringField(required=True)
	avatar   = URLField()
	pockets  = ListField(IntField)

	def __str__(self):
		return str(self.nickname)

class Note(Document):
	author     = ReferenceField(User, required=True)
	anonymous  = BooleanField(required=True, default = True)
	message    = StringField(required = True, max_length=255)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.now, required=True)
	location   = PointField(required=True, auto_index=True)
	expiration = DateTimeField()
	takes      = IntField()
	limit      = IntField(default=-1)
	tags       = ListField(StringField())
	def __str__(self):
		return str(self.timestamp)



class Comment(Document):
	author  = ReferenceField(User, required=True)
	note    = ReferenceField(Note, required=True)
	comment = StringField()

