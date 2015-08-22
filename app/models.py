from mongoengine import * 

class User(Document):
	password = StringField(required=True)
	nickname = StringField(required=True)
	avatar   = URLField()