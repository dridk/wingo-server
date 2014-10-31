from flask import Flask
from flask.ext import restful

class NoteResource(restful.Resource):
    def get(self):
        return {'hello': 'world'}
