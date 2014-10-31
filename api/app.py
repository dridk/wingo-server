from flask import Flask
from flask.ext import restful
from resources.notes import Notes

app = Flask(__name__)
api = restful.Api(app)



api.add_resource(Notes, '/notes')

if __name__ == '__main__':
    app.run(debug=True)