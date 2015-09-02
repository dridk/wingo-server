from flask.ext.script import Manager , Shell
from wingo import create_app
from wingo import models
import dbtools
from test import suite 
import unittest 
import os
import inspect 
from datetime import timedelta

#Create application
#try to use environ variable as config. Use by default devel
app = create_app(os.environ.get("WINGO_CONFIG","devel"))

#app.permanent_session_lifetime = timedelta(minutes=1)

manager = Manager(app, description="manage wingo application")
manager.add_command("dbtools", dbtools.manager)

# def _make_context():
# 	return dict(User = models.User, Note = models.Note, Comm)
# manager.add_command("shell", Shell(make_context=_make_context))




@manager.command 
def test():
	unittest.TextTestRunner(verbosity=2).run(suite)



if __name__ == "__main__":
	manager.run()