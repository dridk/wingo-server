from flask.ext.script import Manager 
from wingo import create_app
import dbtools
from test import suite 
import unittest 
import os

#Create application
#try to use environ variable as config. Use by default devel
app = create_app(os.environ.get("WINGO_CONFIG","devel"))


manager = Manager(app, description="manage wingo application")
manager.add_command("dbtools", dbtools.manager)


@manager.command 
def test():
	unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
	manager.run()