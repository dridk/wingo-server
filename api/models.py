from datetime import datetime
from mongoengine import *

MSG_LENGTH = 255


class User(Document):
	email    = EmailField(required=True)
	password = StringField(required=True)
	nickname = StringField(required=True)
	pockets  = ListField(IntField)

class Note(Document):
	author     = ReferenceField(User, required=True)
	anonymous  = BooleanField(required=True, default = True)
	message    = StringField(required = True, max_length=MSG_LENGTH)
	picture    = URLField()
	timestamp  = DateTimeField(default=datetime.now, required=True)
	location   = PointField(required=True)
	expiration = DateTimeField()
	takes      = IntField()
	limit      = IntField()
	tags       = ListField(StringField())



class Comment(Document):
	author  = ReferenceField(User, required=True)
	comment = StringField()

class Config(Document):
	allowed_radius = ListField(IntField())
	message_length = IntField()
	version        = StringField()