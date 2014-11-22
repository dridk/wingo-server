#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask
from flask.ext import restful
from flask import render_template
import mongoengine as mongo
from models import *

import os

# Transform all exception as a Json Error
# class ExceptionAwareApi(restful.Api):
#     def handle_error(self, e):

#     	message = str(e)
#     	if hasattr(e,"data"):
# 			data = getattr(e, 'data')
# 			if "message" in data:
# 				message = data["message"]

# 	code= 400
# 	results = ErrorResponse(message,code)
# 	return self.make_response(results, code)

''' initialization of application '''
app = Flask(__name__)
api = restful.Api(app)

'''load configuration from config.py '''
app.config.from_pyfile("config.py")
mongo.connect(app.config["DATABASE"])

''' Create upload directory if not present '''
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
	os.makedirs(app.config["UPLOAD_FOLDER"])





@app.before_request
def check_request():
	return

# We want to access app from resources..
from resources.notes import *
from resources.comments import *
from resources.config import *
from resources.tags import *
from resources.users import *

api.add_resource(NoteCollection, '/notes')
api.add_resource(NoteResource, '/notes/<string:note_id>')
api.add_resource(NoteUploadResource, '/notes/picture')
api.add_resource(NoteDownloadResource, '/notes/picture/<string:filename>')

api.add_resource(UserLogin, '/users/login')
api.add_resource(UserLogout, '/users/logout')
api.add_resource(UserMe, '/users/me')
api.add_resource(PocketNote, '/users/pokets')


api.add_resource(CommentCollection, '/notes/<string:note_id>/comments')
#api.add_resource(CommentResource, '/comment/<string:comment_id>')
api.add_resource(ConfigResource, '/config')
api.add_resource(TagResource, '/tags')



	 

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")