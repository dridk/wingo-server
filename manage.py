from flask.ext.script import Manager 
from wingo import create_app
import dbtools

app = create_app("")
manager = Manager(app, description="manage wingo application")
manager.add_command("dbtools", dbtools.manager)



if __name__ == "__main__":
	manager.run()