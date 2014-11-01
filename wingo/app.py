from flask import Flask
from flask.ext import restful
from models import * 
from resources.notes import *

connect('wingo') 
app = Flask(__name__)
api = restful.Api(app)



api.add_resource(NoteCollection, '/notes/search')

if __name__ == '__main__':
    app.run(debug=True)