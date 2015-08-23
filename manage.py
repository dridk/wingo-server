from flask.ext.script import Manager 
from wingo import create_app
import dbtools
from test import suite 
import unittest 

app = create_app("")
manager = Manager(app, description="manage wingo application")
manager.add_command("dbtools", dbtools.manager)


@manager.command 
def test():
	unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
	manager.run()