from flask import Flask
from flask.ext import restful

class Notes(restful.Resource):
    def get(self):
        return {'hello': 'world'}
