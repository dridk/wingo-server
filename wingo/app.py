from flask import Flask
from flask.ext import restful
import mongoengine as mongo
from models import * 
from resources.notes import *
from resources.config import *
from resources.tags import *

app = Flask(__name__)
api = restful.Api(app)

#load configuration from config.py 
app.config.from_pyfile("config.py")
mongo.connect(app.config["DATABASE"])



api.add_resource(NoteCollection, '/notes')
api.add_resource(NoteResource, '/notes/<string:note_id>')
api.add_resource(ConfigResource, '/config')
api.add_resource(TagResource, '/tags')


if __name__ == '__main__':
    app.run(debug=True)