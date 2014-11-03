from flask import Flask
from flask.ext import restful
import mongoengine as mongo
from models import * 
from resources.notes import *
from resources.comments import *
from resources.config import *
from resources.tags import *

class ExceptionAwareApi(restful.Api):
    def handle_error(self, e):

		#code = getattr(e, 'code', 500)
		data = getattr(e, 'data')
		if "message" in data:
			message = data["message"]
		else:
			message = "Unknown Error"
		
		code= 400
		results = {"success":"false", "message": message}
		return self.make_response(results, code)



app = Flask(__name__)
api = ExceptionAwareApi(app)

#load configuration from config.py 
app.config.from_pyfile("config.py")
mongo.connect(app.config["DATABASE"])



api.add_resource(NoteCollection, '/notes')
api.add_resource(NoteResource, '/notes/<string:note_id>')
api.add_resource(CommentCollection, '/notes/<string:note_id>/comments')
#api.add_resource(CommentResource, '/comment/<string:comment_id>')
api.add_resource(ConfigResource, '/config')
api.add_resource(TagResource, '/tags')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")